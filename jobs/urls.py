from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/manage/', views.manage_listings, name='manage_listings'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/import/', views.import_external_jobs, name='import_external_jobs'),
    path('jobs/browse/', views.browse_jobs, name='browse_jobs'),
    path('applications/<int:application_id>/resume/', views.view_resume, name='view_resume'),
    path('applications/<int:application_id>/status/<str:status>/', views.update_application_status, name='update_application_status'),
]


