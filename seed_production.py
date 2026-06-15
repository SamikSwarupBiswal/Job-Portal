import os
import django

# Initialize Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_portal.settings')
django.setup()

from django.contrib.auth import get_user_model
from jobs.models import Job

User = get_user_model()

def seed_data():
    print("Starting database seeding...")

    # 1. Create Users
    # Admin Superuser
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@jobportal.com', 'admin1234')
        admin.role = 'admin'
        admin.save()
        print("Superuser 'admin' created.")
    else:
        admin = User.objects.get(username='admin')
        print("Superuser 'admin' already exists.")

    # Seeker See1
    if not User.objects.filter(username='See1').exists():
        seeker = User.objects.create_user('See1', 'see1@jobportal.com', 'seeker1234')
        seeker.role = 'seeker'
        seeker.save()
        print("Seeker 'See1' created.")
    else:
        print("Seeker 'See1' already exists.")

    # Employer Emp1
    if not User.objects.filter(username='Emp1').exists():
        emp1 = User.objects.create_user('Emp1', 'emp1@jobportal.com', 'employer1234')
        emp1.role = 'employer'
        emp1.save()
        print("Employer 'Emp1' created.")
    else:
        emp1 = User.objects.get(username='Emp1')
        print("Employer 'Emp1' already exists.")

    # Employer Emp2
    if not User.objects.filter(username='Emp2').exists():
        emp2 = User.objects.create_user('Emp2', 'emp2@jobportal.com', 'employer1234')
        emp2.role = 'employer'
        emp2.save()
        print("Employer 'Emp2' created.")
    else:
        emp2 = User.objects.get(username='Emp2')
        print("Employer 'Emp2' already exists.")

    # 2. Create Job Listings
    # 5 jobs for Emp1
    emp1_jobs = [
        ("Software Engineer (Python/Django)", "We are looking for a backend developer skilled in Python and Django to build robust, scalable web services.", "TechCorp Solutions", "New York", "$120,000 - $140,000", "Engineering"),
        ("Lead Data Scientist", "Apply advanced machine learning models, statistical analysis, and data mining to solve complex product problems.", "InsightAnalytics", "Remote", "$150,000 - $170,000", "Data Science"),
        ("Frontend Developer (React)", "Design and build stunning, responsive user interfaces using React, HTML5, CSS3, and Bootstrap.", "CreativeWeb", "San Francisco", "$110,000 - $125,000", "Engineering"),
        ("Product Manager", "Lead product strategy, define feature roadmaps, and collaborate with engineering and design teams to ship premium products.", "InnovateLabs", "Chicago", "$130,000 - $150,000", "Product"),
        ("DevOps Engineer", "Manage cloud infrastructure, CI/CD pipelines, and server deployments on AWS, Kubernetes, and Docker.", "CloudScale", "Remote", "$140,000 - $160,000", "Engineering"),
    ]

    # 5 jobs for Emp2
    emp2_jobs = [
        ("QA Automation Engineer", "Develop and execute automated test suites for web applications using Selenium, pytest, and CI/CD tools.", "QualityFirst Inc.", "Boston", "$95,000 - $115,000", "Quality Assurance"),
        ("UI/UX Product Designer", "Create modern user journeys, wireframes, high-fidelity mockups, and interactive prototypes for SaaS platforms.", "DesignFlow Studio", "Remote", "$105,000 - $125,000", "Product"),
        ("Technical Writer", "Draft, edit, and maintain high-quality API documentation, developer guides, and help center articles.", "DocuDocs", "Austin", "$80,000 - $95,000", "Content"),
        ("Machine Learning Engineer", "Build, train, deploy, and monitor deep learning models for NLP and computer vision tasks in production.", "DeepVision AI", "Seattle", "$145,000 - $165,000", "Data Science"),
        ("HR Generalist", "Coordinate recruitment efforts, manage employee onboarding/offboarding, and implement company culture initiatives.", "TalentHub Partners", "Atlanta", "$75,000 - $88,000", "Product"),
    ]

    # Insert Emp1 jobs
    for title, desc, comp, loc, sal, cat in emp1_jobs:
        if not Job.objects.filter(title=title, company=comp).exists():
            Job.objects.create(
                title=title,
                description=desc,
                company=comp,
                location=loc,
                salary=sal,
                category=cat,
                employer=emp1,
                is_external=False
            )
            print(f"Created job: '{title}' for Emp1")

    # Insert Emp2 jobs
    for title, desc, comp, loc, sal, cat in emp2_jobs:
        if not Job.objects.filter(title=title, company=comp).exists():
            Job.objects.create(
                title=title,
                description=desc,
                company=comp,
                location=loc,
                salary=sal,
                category=cat,
                employer=emp2,
                is_external=False
            )
            print(f"Created job: '{title}' for Emp2")

    # 3. Trigger External Job Import
    # Import first page from API
    import requests
    url = "https://www.themuse.com/api/public/jobs?page=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            jobs_data = data.get('results', [])
            for item in jobs_data[:20]:
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
                        employer=admin,
                        is_external=True,
                        external_url=external_url
                    )
            print("Successfully imported external API jobs.")
    except Exception as e:
        print(f"Failed to import external jobs: {e}")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
