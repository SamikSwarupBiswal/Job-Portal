from django.utils.http import MAX_URL_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

#User Model
class User(AbstractUser):
    ROLE_CHOICES=(('seeker','Job Seeker'),('employer', 'Employer'),('admin','Admin'),)
    role=models.CharField(max_length=10,choices=ROLE_CHOICES, default='seeker')

    def is_seeker(self):
        return self.role=='seeker'
    
    def is_employer(self):
        return self.role=='employer'
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Job listing model
class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company =models.CharField(max_length=255)
    location =models.CharField(max_length=255)
    salary = models.CharField(max_length=100, blank=True, null=True)# In case the salary is negotiable
    category=models.CharField(max_length=100)
    
    #linked to employer

    employer=models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Fields to handle external API integrations
    is_external = models.BooleanField(default=False)
    external_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

#Application Model
class Application(models.Model):
    STATUS_CHOICES=(('pending','Pending'),('accepted', 'Accepted'),('rejected','Rejected'),)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    seeker=models.ForeignKey(User,on_delete=models.CASCADE,related_name='applications')
    cover_letter=models.TextField(blank=True) #For typing cover letter
    resume=models.FileField(upload_to='resumes/',blank=True,null=True) #For uploading file
    applied_at=models.DateTimeField(auto_now_add=True) #To note time and date of when was job applied
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"{(self.seeker.username)} applied for {(self.job.title)}"
    