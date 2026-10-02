from django.test import TestCase
from django.urls import reverse

from .forms import StudentForm
from .models import Student


def payload(**overrides):
    data = {
        "student_id": "STU-2026-001",
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "+1 555 123 4567",
        "address": "123 Main Street",
        "city": "Springfield",
        "state": "Illinois",
        "postal_code": "62704",
        "country": "USA",
        "course": "B.Sc Computer Science",
        "department": "Engineering",
        "enrollment_year": 2026,
        "is_active": "on",
    }
    data.update(overrides)
    return data


class StudentModelTests(TestCase):
    def test_create_and_str(self):
        student = Student.objects.create(
            student_id="STU-1",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+15551234567",
            address="123 Main Street",
        )
        self.assertEqual(str(student), "Jane Doe (STU-1)")
        self.assertIsNotNone(student.created_at)

    def test_student_id_unique(self):
        Student.objects.create(
            student_id="STU-1",
            first_name="A",
            last_name="B",
            email="a@example.com",
            phone="1234567",
            address="x",
        )
        with self.assertRaises(Exception):
            Student.objects.create(
                student_id="STU-1",
                first_name="C",
                last_name="D",
                email="c@example.com",
                phone="1234567",
                address="x",
            )


class StudentFormTests(TestCase):
    def test_valid_form(self):
        self.assertTrue(StudentForm(data=payload()).is_valid())

    def test_duplicate_student_id_rejected(self):
        Student.objects.create(
            student_id="STU-2026-001",
            first_name="Old",
            last_name="Record",
            email="old@example.com",
            phone="1234567",
            address="x",
        )
        form = StudentForm(data=payload(email="new@example.com"))
        self.assertFalse(form.is_valid())
        self.assertIn("student_id", form.errors)

    def test_bad_phone_rejected(self):
        form = StudentForm(data=payload(phone="not-a-phone"))
        self.assertFalse(form.is_valid())
        self.assertIn("phone", form.errors)


class StudentViewTests(TestCase):
    def test_list_page(self):
        response = self.client.get(reverse("student_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No students yet")

    def test_create_flow_persists_record(self):
        response = self.client.post(reverse("student_create"), data=payload())
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(student_id="STU-2026-001").exists())

        detail = self.client.get(response["Location"])
        self.assertContains(detail, "Jane")

    def test_detail_and_delete(self):
        student = Student.objects.create(
            student_id="STU-9",
            first_name="Jane",
            last_name="Doe",
            email="jane@example.com",
            phone="+15551234567",
            address="123 Main Street",
        )
        self.assertEqual(
            self.client.get(reverse("student_detail", args=[student.pk])).status_code, 200
        )
        response = self.client.post(reverse("student_delete", args=[student.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())
