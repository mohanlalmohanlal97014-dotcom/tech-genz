from django.contrib import admin

# Register your models here.
from .models import Profile, Company, Internship, InternshipApplication


admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Internship)
admin.site.register(InternshipApplication)