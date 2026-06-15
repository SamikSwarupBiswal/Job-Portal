from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse, Http404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, JobForm
from .models import User, Job, Application
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q

# Create your views here.
# Home Page View (Clean Landing Page)
def home(request):
    return render(request, 'jobs/home.html')

from django.core.paginator import Paginator

# Browse Jobs Page View with Search & Filters
def browse_jobs(request):
    # Fetch all jobs ordered by newest
    jobs = Job.objects.all().order_by('-created_at')
    
    # Get parameters from URL query string
    query = request.GET.get('query', '')
    location = request.GET.get('location', '')
    category = request.GET.get('category', '')
    
    # Filter by search keywords in title, description, or company
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) | 
            Q(company__icontains=query)
        )
        
    # Filter by exact location
    if location:
        jobs = jobs.filter(location__iexact=location)
        
    # Filter by exact category
    if category:
        jobs = jobs.filter(category__iexact=category)
        
    # Fetch unique categories and locations for dynamic filters
    all_categories = Job.objects.values_list('category', flat=True).distinct()
    all_locations = Job.objects.values_list('location', flat=True).distinct()

    # Interleave: 1 API (external), 1 Employer (internal)...
    api_jobs = list(jobs.filter(is_external=True))
    employer_jobs = list(jobs.filter(is_external=False))
    
    interleaved_jobs = []
    if len(api_jobs) > 0 and len(employer_jobs) > 0:
        max_len = max(len(api_jobs), len(employer_jobs))
        for idx in range(max_len):
            interleaved_jobs.append(api_jobs[idx % len(api_jobs)])
            interleaved_jobs.append(employer_jobs[idx % len(employer_jobs)])
    elif len(api_jobs) > 0:
        interleaved_jobs = api_jobs
    else:
        interleaved_jobs = employer_jobs

    # Paginate listings to 12 jobs per page
    paginator = Paginator(interleaved_jobs, 12)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    context = {
        'jobs': jobs_page,
        'categories': all_categories,
        'locations': all_locations,
        'query': query,
        'selected_location': location,
        'selected_category': category,
    }
    return render(request, 'jobs/browse_jobs.html', context)

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)  
            return redirect('home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'jobs/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
        
    return render(request, 'jobs/login.html', {'form': form})


# User Logout View
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return redirect('home') # Fallback 

# Post a Job (Only for Employers)
@login_required # Redirects to login page if user isn't logged in
def post_job(request):
    # Security Check: Reject job seekers from viewing this page
    if request.user.role == 'seeker':
        return redirect('home')
        
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)  # Don't save to DB yet
            job.employer = request.user    # Assign current logged-in user as employer
            job.save()                     # Now save to DB
            return redirect('home')
    else:
        form = JobForm()
        
    return render(request, 'jobs/post_job.html', {'form': form})

# Manage Job Listings (Dashboard for Employers to see applicants)
@login_required
def manage_listings(request):
    if request.user.role == 'seeker':
        return redirect('home')
        
    # Get all jobs posted by this employer
    my_jobs = Job.objects.filter(employer=request.user).order_by('-created_at')
    return render(request, 'jobs/manage_listings.html', {'jobs': my_jobs})
# Job Detail View
def job_detail(request, job_id):
    # Fetch the job, or return 404 error if it doesn't exist
    job = get_object_or_404(Job, pk=job_id)
    has_applied = False
    if request.user.is_authenticated and request.user.role == 'seeker':
        has_applied = Application.objects.filter(job=job, seeker=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})


# Apply for a Job View
@login_required
def apply_job(request, job_id):
    if request.user.role != 'seeker':
        return redirect('job_detail', job_id=job_id)
        
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if application already exists to prevent duplicate submissions
    if Application.objects.filter(job=job, seeker=request.user).exists():
        return redirect('job_detail', job_id=job_id)
        
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')  # Read the uploaded file
        
        # Create and save the Application object
        Application.objects.create(
            job=job,
            seeker=request.user,
            cover_letter=cover_letter,
            resume=resume
        )
        return redirect('job_detail', job_id=job_id)
    return redirect('job_detail', job_id=job_id)

# Import External Jobs View (Only for Superusers/Admins)
@login_required
def import_external_jobs(request):
    # Security: Ensure only superusers/admins can trigger the import
    if not request.user.is_superuser:
        return redirect('home')
        
    # Clear out previously imported external jobs to clean up old German listings
    Job.objects.filter(is_external=True).delete()
        
    # Using The Muse API to fetch English job listings
    url = "https://www.themuse.com/api/public/jobs?page=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs_data = data.get('results', [])
            
            # Find an admin user to assign as the job owner
            admin_user = User.objects.filter(is_superuser=True).first()
            if not admin_user:
                admin_user = request.user
                
            for item in jobs_data[:20]:  # Limit import to top 20 listings
                # Fetch details mapping to The Muse API response format
                external_url = item.get('refs', {}).get('landing_page')
                if external_url and not Job.objects.filter(external_url=external_url).exists():
                    locations = item.get('locations', [])
                    location_name = locations[0].get('name', 'Remote') if locations else 'Remote'
                    
                    categories = item.get('categories', [])
                    category_name = categories[0].get('name', 'General') if categories else 'General'
                    
                    Job.objects.create(
                        title=item.get('name', 'External Job'),
                        description=item.get('contents', 'Refer to external website.'),
                        company=item.get('company', {}).get('name', 'Unknown Company'),
                        location=location_name,
                        salary='Not specified',
                        category=category_name,
                        employer=admin_user,
                        is_external=True,
                        external_url=external_url
                    )
    except Exception:
        # Fail silently and redirect in case of API timeout or error
        pass
        
    return redirect('browse_jobs')


# View candidate resume (secured, requires login)
@login_required
def view_resume(request, application_id):
    application = get_object_or_404(Application, pk=application_id)
    if not application.resume:
        raise Http404("Resume not found.")
    
    return FileResponse(application.resume.open())


# Update candidate application status (Only for Employers who own the job)
@login_required
def update_application_status(request, application_id, status):
    if request.user.role != 'employer':
        return redirect('home')
        
    application = get_object_or_404(Application, pk=application_id)
    
    # Security: Ensure this employer posted the job
    if application.job.employer != request.user:
        return redirect('home')
        
    if status in ['pending', 'accepted', 'rejected']:
        application.status = status
        application.save()
        
    return redirect('manage_listings')


