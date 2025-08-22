from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
from cloudinary.models import CloudinaryField 
from django.utils.html import format_html


# =====================
# 1. Services Offered & Selected
# =====================
class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

# =====================
# 2. Patient Information
# =====================

class Patient(models.Model):
    username = models.CharField(max_length=300, unique=True, blank=True)
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        if not self.username:
            random_id = str(uuid.uuid4())[:6]  # short unique ID
            self.username = f"{self.first_name.lower()}{self.last_name.lower()}_{random_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(Patient, on_delete=models.CASCADE)
    dob = models.DateField()
    birth_sex = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    gender_identity = models.CharField(max_length=30, choices=[('Straight', 'Straight'),('Lesbian', 'Lesbian'), ('Gay', 'Gay'), ('Transgender', 'Transgender'), ('Bisexual', 'Bisexual')])
    email = models.EmailField()
    primary_phone = models.CharField(max_length=15)
    address = models.TextField()
    po_box = models.CharField(max_length=300, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=300, null=True, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, null=True, blank=True)
    services = models.ManyToManyField(Service, blank=True)

    insurance_id = models.CharField(max_length=300, null=True, blank=True)
    insurance_company = models.CharField(max_length=300, null=True, blank=True)
    policy_group = models.CharField(max_length=300, null=True, blank=True)
    policy_holder_name = models.CharField(max_length=300, null=True, blank=True)
    policy_holder_relationship = models.CharField(max_length=50, null=True, blank=True)
    policy_holder_dob = models.DateField(null=True, blank=True)
    policy_holder_address = models.TextField(null=True, blank=True)
    policy_holder_phone = models.CharField(max_length=15, null=True, blank=True)

    profile_image = CloudinaryField('image', blank=True, null=True)
    
    def image_tag(self):
        if self.profile_image:
            return format_html('<img src="{}" width="400" height="400" style="border-radius:8px;" />', self.profile_image.url)
        return "No image"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    image = CloudinaryField('image', blank=True, null=True)
    designation = models.CharField(max_length=255)   # e.g., "Board-Certified Psychiatrist"
    experience = models.PositiveIntegerField(default=0)  # store number of years
    stars = models.PositiveIntegerField(default=0)  # store number of stars (1–5)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)  # e.g., 4.7

    def image_tag(self):
        if self.image:
            return format_html(
                '<img src="{}" width="150" height="150" style="border-radius:8px;" />', 
                self.image.url
            )
        return "No image"

    def __str__(self):
        return self.name





