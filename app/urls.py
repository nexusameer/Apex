from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('contact', ContactView.as_view(), name='contact'),
    path('start/', views.create_patient, name='create_patient'),
    path('profile/<int:patient_id>/', views.create_profile, name='create_profile'),
    path('select_services/<str:username>/', views.select_services, name='select_services'),

    path('about', AboutView.as_view(), name = 'about'),
    path('doctor', DoctorView.as_view(), name = 'doctor'),
    path('terms', TermsView.as_view(), name = 'terms'),
    path('services', ServiceView.as_view(), name = 'service'),
    path('error', ErrorView.as_view(), name = 'error'),
    path('appointment', AppointmentView.as_view(), name = 'appointment')

]
