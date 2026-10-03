from django.contrib import messages
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student

LIST_CACHE_KEY = "students:all"
LIST_CACHE_TTL = 15


def get_all_students():
    rows = cache.get(LIST_CACHE_KEY)
    if rows is None:
        rows = list(Student.objects.all())
        cache.set(LIST_CACHE_KEY, rows, LIST_CACHE_TTL)
    return rows


def student_list(request):
    query = request.GET.get("q", "").strip()
    rows = get_all_students()
    total = len(rows)
    if query:
        needle = query.lower()
        rows = [
            s
            for s in rows
            if any(
                needle in str(getattr(s, f) or "").lower()
                for f in (
                    "student_id",
                    "first_name",
                    "last_name",
                    "email",
                    "phone",
                    "city",
                )
            )
        ]
    context = {"students": rows, "query": query, "total": total}
    return render(request, "students/student_list.html", context)


def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            cache.delete(LIST_CACHE_KEY)
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
    cache_key = f"students:detail:{pk}"
    student = cache.get(cache_key)
    if student is None:
        student = get_object_or_404(Student, pk=pk)
        cache.set(cache_key, student, LIST_CACHE_TTL)
    return render(request, "students/student_detail.html", {"student": student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        name = str(student)
        student.delete()
        cache.delete(LIST_CACHE_KEY)
        cache.delete(f"students:detail:{pk}")
        messages.success(request, f"Deleted {name}.")
        return redirect("student_list")
    return render(request, "students/student_confirm_delete.html", {"student": student})
