"""
URL configuration for intern project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',views.home,name='home'),
    path('companies/',views.companies_info,name='companies-info'),
    path('internship-info',views.internship_info,name='internship-info'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.register, name='register'),
    path('company-dashboard/', views.company_dashboard, name='company-dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student-dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('add-company/', views.add_company, name='add-company'),
    path("company/<int:profile_id>/", views.view_company_profile, name="view-company-profile"),
    path('company-list/', views.company_list, name='company-list'),
    path('student-profile/', views.student_profile, name='student-profile'),
    path('internships/', views.internship_list, name='internships'),
    path('post-internship/', views.post_internship, name='post-internship'),
    path('internship/<int:internship_id>/', views.internship_detail, name='internship-detail'),
    path('apply-internship/<int:internship_id>/', views.apply_internship, name='apply-internship'),
    path('view-applications/', views.view_applications, name='view-applications'),
    path('my-applications/', views.my_applications, name='my-applications'),
    path('update-application-status/<int:application_id>/<str:status>/', views.update_application_status, name='update-application-status'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

