from django import forms

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_of_birth",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "course",
            "department",
            "enrollment_year",
            "is_active",
        ]
        widgets = {
            "student_id": forms.TextInput(attrs={"placeholder": "STU-2026-001"}),
            "first_name": forms.TextInput(attrs={"placeholder": "Jane"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Doe"}),
            "email": forms.EmailInput(attrs={"placeholder": "jane.doe@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "+1 555 123 4567"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.TextInput(attrs={"placeholder": "123 Main Street"}),
            "city": forms.TextInput(attrs={"placeholder": "Springfield"}),
            "state": forms.TextInput(attrs={"placeholder": "Illinois"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "62704"}),
            "country": forms.TextInput(attrs={"placeholder": "USA"}),
            "course": forms.TextInput(attrs={"placeholder": "B.Sc Computer Science"}),
            "department": forms.TextInput(attrs={"placeholder": "Engineering"}),
            "enrollment_year": forms.NumberInput(attrs={"placeholder": "2026", "min": 2000}),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data["student_id"].strip().upper()
        qs = Student.objects.filter(student_id__iexact=student_id)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A student with this ID already exists.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = Student.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A student with this email already exists.")
        return email
