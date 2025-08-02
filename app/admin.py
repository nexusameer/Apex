from django.contrib import admin
from .models import *


admin.site.site_header = "APEX Admin Panel"
admin.site.site_title = "APEX"
admin.site.index_title = "Welcome to APEX Dashboard"

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 25


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('first_name', 'last_name')
    list_per_page = 25


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'first_name', 'last_name', 'dob', 'birth_sex', 'gender_identity',
        'email', 'primary_phone'
    )
    search_fields = (
        'user__first_name', 'user__last_name', 'email',
        'primary_phone', 'insurance_company', 'policy_holder_name'
    )
    list_filter = ('birth_sex', 'gender_identity', 'insurance_company')
    autocomplete_fields = ['user', 'services']

    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'dob', 'birth_sex', 'gender_identity', 'email', 'primary_phone', 'address', 'po_box', 'profile_image', 'image_tag')
        }),
        ('Emergency Contact', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone')
        }),
        ('Services Selected', {
            'fields': ('services',)
        }),
        ('Insurance Details', {
            'fields': (
                'insurance_id', 'insurance_company', 'policy_group',
                'policy_holder_name', 'policy_holder_relationship',
                'policy_holder_dob', 'policy_holder_address', 'policy_holder_phone'
            )
        }),
    )
    readonly_fields = ('image_tag',) 

    list_per_page = 20

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    first_name.admin_order_field = 'user__first_name'
    first_name.short_description = 'First Name'

    last_name.admin_order_field = 'user__last_name'
    last_name.short_description = 'Last Name'
