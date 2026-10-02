from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse

phone_validator = RegexValidator(
    regex=r"^\+?[\d\s\-().]{7,20}$",
    message="Enter a valid phone number, e.g. +1 555 123 4567.",
)


class Student(models.Model):
    student_id = models.CharField("Student ID", max_length=20, unique=True)
    first_name = models.CharField("First name", max_length=60)
    last_name = models.CharField("Last name", max_length=60)
    email = models.EmailField("Email", unique=True)
    phone = models.CharField("Phone", max_length=20, validators=[phone_validator])

    date_of_birth = models.DateField("Date of birth", null=True, blank=True)
    address = models.CharField("Street address", max_length=255)
    city = models.CharField("City", max_length=100, blank=True)
    state = models.CharField("State / Province", max_length=100, blank=True)
    postal_code = models.CharField("Postal code", max_length=20, blank=True)
    country = models.CharField("Country", max_length=100, blank=True)

    course = models.CharField("Course / Program", max_length=120, blank=True)
    department = models.CharField("Department", max_length=120, blank=True)
    enrollment_year = models.PositiveIntegerField("Enrollment year", null=True, blank=True)
    is_active = models.BooleanField("Currently enrolled", default=True)

    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def get_absolute_url(self):
        return reverse("student_detail", args=[self.pk])
