from django.contrib import admin
from .models import Department, Doctor, DepartmentService

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'department',
        'role',
        'experience',
        'rating',
        'is_available'
    )
    list_filter = ('department', 'is_available')
    search_fields = ('name', 'department__name')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DepartmentService)
class DepartmentServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'order')
    list_filter = ('department',)
    search_fields = ('name', 'department__name')