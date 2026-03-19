from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import InternshipApplication, Profile, Company, Internship, Application
from django.contrib import messages

def home(request):
    return render(request,'home.html')

def internship_info(request):
    return render(request,'internship-info.html')

def companies_info(request):
    return render(request,'companies.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        phoneNo = request.POST.get('phoneNo')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            name=name,
            role=role,
            phoneNo=phoneNo
        )

        return redirect('login')

    return render(request, 'profile.html')

from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            profile = Profile.objects.filter(user=user).first()

            if not profile:
                messages.error(request, "Profile not found")
                return redirect('login')

            if profile.role == "company":
                return redirect('company-dashboard')
            else:
                return redirect('student-dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def company_dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != "company":
        return redirect("student-dashboard")

    company = Company.objects.filter(profile=profile).first()

    return render(request, 'company-dashboard.html', {
        'company': company,
        'profile': profile
    })
    
@login_required
def add_company(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != "company":
        return redirect("student-dashboard")

    existing_company = Company.objects.filter(profile=profile).first()

    if existing_company:
        return redirect('company-dashboard')

    if request.method == "POST":
        company_name = request.POST.get("company_name")
        website = request.POST.get("website")
        description = request.POST.get("description")

        Company.objects.create(
            profile=profile,
            company_name=company_name,
            website=website,
            description=description
        )

        return redirect('company-dashboard')

    return render(request, "add_company.html")   

from django.shortcuts import render, get_object_or_404

def view_company_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, role="company")
    company = get_object_or_404(Company, profile=profile)

    context = {
        "profile": profile,
        "company": company
    }

    return render(request, "company-profile.html", context)  

@login_required
def company_list(request):

    profile = get_object_or_404(Profile,user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    companies = Company.objects.filter(approved=True)

    search = request.GET.get('search')

    if search:
        companies = companies.filter(company_name__icontains=search)

    return render(request,'comProfile.html',{
        'companies':companies
    })
    
@login_required
def student_dashboard(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    return render(request, 'student-dashboard.html', {'profile': profile})
    
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def student_profile(request):

    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    if request.method == "POST":

        if request.FILES.get("profile_photo"):
            profile.profile_photo = request.FILES.get("profile_photo")
            profile.save()

    return render(request, 'student-profile.html', {'profile': profile})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def post_internship(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Allow only company role
    if profile.role != "company":
        return redirect("student-dashboard")

    # Get company linked to this profile
    company = get_object_or_404(Company, profile=profile)

    if request.method == "POST":
        title = request.POST.get("title")
        location = request.POST.get("location")
        stipend = request.POST.get("stipend")
        duration = request.POST.get("duration")
        description = request.POST.get("description")
        skills_required = request.POST.get("skills_required")

        Internship.objects.create(
            company_name=company,
            title=title,
            location=location,
            stipend=stipend,
            duration=duration,
            description=description,
            skills_required=skills_required
        )

        return redirect("company-dashboard")

    return render(request, "post-internship.html")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Internship, Profile


@login_required
def internship_list(request):

    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    internships = Internship.objects.filter(
        company_name__approved=True
    ).order_by("-created_at")

    # SEARCH + FILTERS
    search = request.GET.get("search")
    company = request.GET.get("company")
    location = request.GET.get("location")
    stipend = request.GET.get("stipend")

    if search:
        internships = internships.filter(title__icontains=search)

    if company:
        internships = internships.filter(
            company_name__company_name__icontains=company
        )

    if location:
        internships = internships.filter(location__icontains=location)

    if stipend:
        internships = internships.filter(stipend__icontains=stipend)

    return render(request, "view-internships.html", {
        "internships": internships
    })

@login_required
def internship_detail(request, internship_id):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    internship = get_object_or_404(
        Internship,
        id=internship_id,
        company_name__approved=True
    )

    return render(request, 'internship-detail.html', {
        'internship': internship
    })

@login_required
def apply_internship(request, internship_id):
    profile = get_object_or_404(Profile, user=request.user)

    if profile.role != "user":
        return redirect("company-dashboard")

    internship = get_object_or_404(
        Internship,
        id=internship_id,
        company_name__approved=True
    )

    already_applied = InternshipApplication.objects.filter(
        internship=internship,
        student=profile
    ).exists()

    if already_applied:
        messages.warning(request, "You have already applied for this internship.")
        return redirect("internship-detail", internship_id=internship.id)
    
    else:
        if request.method == "POST":
            resume = request.FILES.get("resume")
            
            InternshipApplication.objects.create(
                internship=internship,
                student=profile,
                resume=resume
                )
            messages.success(request, "Application submitted successfully!")
            return redirect("internship-detail", internship_id=internship.id)
        return render(request, "apply-internship.html", {
            "internship": internship
            })

@login_required
def view_applications(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Allow only company role
    if profile.role != "company":
        return redirect("student-dashboard")

    # Get company linked to profile
    company = get_object_or_404(Company, profile=profile)

    # Get applications for internships posted by this company
    applications = InternshipApplication.objects.filter(
        internship__company_name=company
    ).select_related("student", "internship").order_by("-applied_at")

    return render(request, "view-applications.html", {
        "applications": applications
    })   


@login_required
def my_applications(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Allow only students
    if profile.role != "user":
        return redirect("company-dashboard")

    applications = InternshipApplication.objects.filter(
        student=profile
    ).select_related("internship", "internship__company_name") \
     .order_by("-applied_at")

    return render(request, "my-applications.html", {
        "applications": applications
    })    


@login_required
def update_application_status(request, application_id, status):
    profile = get_object_or_404(Profile, user=request.user)

    # Only company can update
    if profile.role != "company":
        return redirect("student-dashboard")

    application = get_object_or_404(InternshipApplication, id=application_id)

    if status == "Accepted":
        application.status = "Accepted"
    elif status == "Rejected":
        application.status = "Rejected"

    application.save()

    messages.success(request, "Application status updated successfully.")

    return redirect("view-applications")    