from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Lecturer, Student, Class, AttendanceRecord, Grade, Enrollment  # Import your Lecturer and Student models
from django.contrib.auth.hashers import check_password

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # Extract role from the clicked button

        if role == 'lecturer':
            lecturer = Lecturer.objects.filter(Username=username).first()
            if lecturer.Username == username and lecturer.Password == password:
                return redirect('lecturer_dashboard')
            else:
                messages.error(request, "Invalid credentials for Lecturer.")

        elif role == 'student':
            student = Student.objects.filter(Username=username).first()
            if student.Username == username and student.Password == password:
                return redirect('student_dashboard')
            
            else:
                messages.error(request, "Invalid credentials for Student.")

    else:
        messages.error(request, "Invalid credentials.")
    return render(request, 'login.html')

def student_dashboard(request):
    return render(request, 'dashboard_student.html')

def lecturer_dashboard(request):
    if request.method == "POST":
        # Extract data from the form
        student_id = request.POST.get("studentId")
        class_id = request.POST.get("classId")

        print("Student")
        print(student_id)
        print("CLass")
        print(class_id)

        try:
            # Fetch the Student and Class instances
            student = Student.objects.get(StudentID=student_id)
            class_instance = Class.objects.get(ClassID=class_id)

            # Check if the enrollment already exists
            if Enrollment.objects.filter(StudentID=student, ClassID=class_instance).exists():
                messages.error(request, "This student is already enrolled in the class.")
            else:
                # Create the enrollment
                Enrollment.objects.create(StudentID=student, ClassID=class_instance)
                messages.success(request, f"{student.Firstname} successfully enrolled in {class_instance.ClassName}!")

        except Student.DoesNotExist:
            messages.error(request, "Invalid student selected.")
        except Class.DoesNotExist:
            messages.error(request, "Invalid class selected.")

        return redirect('lecturer_dashboard')  # Redirect to the same page after processing

    students = Student.objects.all()
    classes = Class.objects.all()
    context = {
        'students': students,
        'classes': classes,
    }

    return render(request, 'dashboard_lecturer.html', context)
