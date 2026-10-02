from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student


def student_list(request):
    query = request.GET.get("q", "").strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(student_id__icontains=query)
            | Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(city__icontains=query)
        )
    context = {"students": students, "query": query, "total": Student.objects.count()}
    return render(request, "students/student_list.html", context)


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Saved {student} to the database.")
            return redirect("student_detail", pk=student.pk)
    else:
        form = StudentForm()
    return render(
        request,
        "students/student_form.html",
        {"form": form, "title": "Add student", "button_label": "Save student"},
    )


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, "students/student_detail.html", {"student": student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        name = str(student)
        student.delete()
        messages.success(request, f"Deleted {name}.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})
