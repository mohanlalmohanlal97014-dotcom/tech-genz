from django.db import models

# Create your models here.

from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    ROLE_CHOICES = (
        ('user','User'),
        ('company','Company'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES)
    phoneNo = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Company(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    website = models.URLField()
    description = models.TextField()
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.company_name
    
class Internship(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.CharField(max_length=200)
    company_name = models.ForeignKey(Company, on_delete=models.CASCADE)
    stipend = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Application(models.Model):
    student_name = models.ForeignKey(Profile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    applied_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student_name} - {self.internship.title}"    
    
class InternshipApplication(models.Model):
    internship = models.ForeignKey(Internship, on_delete=models.CASCADE)
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.student.name    