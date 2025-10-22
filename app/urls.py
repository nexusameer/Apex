from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact', ContactView.as_view(), name='contact'),
    path('start/', views.create_patient, name='create_patient'),
    path('profile/<int:patient_id>/', views.create_profile, name='create_profile'),
    path('select_services/<str:username>/', views.select_services, name='select_services'),

    path('about', AboutView.as_view(), name='about'),
    path('doctors', DoctorView.as_view(), name='doctors'),
    path('terms', TermsView.as_view(), name='terms'),
    path('services', ServiceView.as_view(), name='services'),
    path('success', SuccessView.as_view(), name='success'),
    path('appointment', AppointmentView.as_view(), name='appointment'),
    path('doctors/<int:doctor_id>/', DoctorDetailView.as_view(), name='doctor_detail'),

    path('privacy-policy', PrivacyPolicyView.as_view(), name='privacy_policy'),

    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:pk>/', views.blog_detail, name='blog_detail'),
]
