from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "course",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "department", "country")
    search_fields = ("student_id", "first_name", "last_name", "email", "phone")
    ordering = ("-created_at",)
