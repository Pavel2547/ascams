from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.urls import reverse
from .models import Lecturer, Student, Class, AttendanceRecord, Grade, Enrollment  # Import your Lecturer and Student models

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
    if request.method == "POST":
        # Extract data from the form
        date = request.POST.get("date")
        time = request.POST.get("time")
        enrollment_id = request.POST.get("enrollment_id")
        attendance_status = request.POST.get("attendance_status")

        enrollment_object = Enrollment.objects.get(EnrollmentID=enrollment_id)

        # Create the enrollment
        AttendanceRecord.objects.create(Date=date, Time=time, EnrollmentID=enrollment_object, AttendanceStatus=attendance_status)
        # messages.success(request, f"{student.Firstname} successfully enrolled in {class_instance.ClassName}!")

        return redirect('student_dashboard')  # Redirect to the same page after processing

    enrollments = Enrollment.objects.all()
    context = {
        'enrollments': enrollments,
    }

    return render(request, 'dashboard_student.html', context)

def lecturer_dashboard(request):
    if request.method == "POST":
        action = request.POST.get('action')

        if action == "enrollment":
            # Extract data from the form
            student_id = request.POST.get("studentId")
            class_id = request.POST.get("classId")
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
        
        elif action == "grade_calculator":

            class_id = request.POST.get("classId")
            return redirect(reverse('calculate_final_grade', kwargs={'class_id': class_id}))

    students = Student.objects.all()
    classes = Class.objects.all()
    context = {
        'students': students,
        'classes': classes,
    }

    return render(request, 'dashboard_lecturer.html', context)

# def calculate_final_grade(request):
#     """
#     Calculate final grades for all enrollments in a specific class.

#     Args:
#         request: The HTTP request object.
#         class_id: The ID of the class.

#     Returns:
#         Render or Redirect: Renders a success/failure page or redirects to a class list.
#     """

#     # Get the class object
#     if request.method == "POST":
#         action = request.POST.get('action')

#         if action == "grade_calculation":
#             class_object = request.POST.get("ClassID")

#             # Get the session count for the class
#             total_sessions = class_object.SessionNumber

#             if total_sessions == 0:
#                 messages.error(request, "Session count for the class is zero. Cannot calculate grades.")
#                 return redirect('class_list')  # Redirect to a class list view (replace 'class_list' as needed)

#             # Get all enrollments for the class
#             enrollments = Enrollment.objects.filter(ClassID=class_object)

#             # Prepare grade updates
#             grade_updates = []

#             for enrollment in enrollments:
#                 # Get all attendance records for this enrollment
#                 attendance_records = AttendanceRecord.objects.filter(EnrollmentID=enrollment)

#                 # Count the 'Present' status
#                 present_count = attendance_records.filter(AttendanceStatus='Present').count()

#                 # Calculate attendance percentage
#                 attendance_percentage = (present_count / total_sessions) * 100

#                 # Determine the grade based on attendance percentage
#                 if attendance_percentage >= 80:
#                     final_grade = "A"
#                 elif attendance_percentage >= 70:
#                     final_grade = "B"
#                 elif attendance_percentage >= 60:
#                     final_grade = "C"
#                 elif attendance_percentage >= 50:
#                     final_grade = "D"
#                 else:
#                     final_grade = "F"

#                 # Update or create the Grade object for this enrollment
#                 grade_obj, created = Grade.objects.update_or_create(
#                     EnrollmentID=enrollment,
#                     defaults={'FinalGrade': final_grade}
#                 )

#                 # Add details to updates list for display
#                 grade_updates.append({
#                     "student_name": f"{enrollment.StudentID.Firstname} {enrollment.StudentID.Surname}",
#                     "class_name": class_object.ClassName,
#                     "attendance_percentage": attendance_percentage,
#                     "final_grade": final_grade
#                 })
            
#     # Render a success page with grade details
#     return render(request, 'grades/calculate_final_grade.html', {
#         "class_name": class_object.ClassName,
#         "grade_updates": grade_updates
#     })

def calculate_final_grade(request, class_id):
    # Get the class object
    class_obj = get_object_or_404(Class, ClassID=class_id)

    # Get the total session count for the class
    total_sessions = class_obj.SessionNumber

    if total_sessions == 0:
        messages.error(request, "Session count for the class is zero. Cannot calculate grades.")
        return redirect('class_list')  # Redirect to a class list view (replace 'class_list' as needed)

    # Get all enrollments for the class
    enrollments = Enrollment.objects.filter(ClassID=class_obj)

    # Prepare grade updates
    grade_updates = []

    for enrollment in enrollments:
        # Get attendance records for this specific student in the class
        attendance_records = AttendanceRecord.objects.filter(EnrollmentID=enrollment)

        # Count the 'Present' status for the student
        present_count = attendance_records.filter(AttendanceStatus='Present').count()

        # Calculate attendance percentage
        attendance_percentage = (present_count / total_sessions) * 100

        # Determine the grade based on attendance percentage
        if attendance_percentage >= 80:
            final_grade = "A"
        elif attendance_percentage >= 70:
            final_grade = "B"
        elif attendance_percentage >= 60:
            final_grade = "C"
        elif attendance_percentage >= 50:
            final_grade = "D"
        else:
            final_grade = "F"

        # Update or create the Grade object for this student's enrollment
        grade_obj, created = Grade.objects.update_or_create(
            EnrollmentID=enrollment,
            defaults={'FinalGrade': final_grade}
        )

        # Add details to updates list for display
        grade_updates.append({
            "student_name": f"{enrollment.StudentID.Firstname} {enrollment.StudentID.Surname}",
            "class_name": class_obj.ClassName,
            "attendance_percentage": attendance_percentage,
            "final_grade": final_grade
        })

    # Render a success page with grade details
    return render(request, 'calculate_final_grade.html', {
        "class_name": class_obj.ClassName,
        "grade_updates": grade_updates
    })
