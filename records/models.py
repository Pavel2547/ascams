from django.db import models

# Lecturer Model
class Lecturer(models.Model):
    LecturerID = models.AutoField(primary_key=True)
    Firstname = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)
    Password = models.CharField(max_length=255)
    Username = models.CharField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return f"{self.Firstname} {self.Surname}"

    def save(self, *args, **kwargs):
        # Auto-generate username before saving
        self.Username = f"{self.Firstname}{self.Surname}".lower()
        super().save(*args, **kwargs)


# Student Model
class Student(models.Model):
    StudentID = models.AutoField(primary_key=True)
    Firstname = models.CharField(max_length=100)
    Surname = models.CharField(max_length=100)
    Password = models.CharField(max_length=255)
    Username = models.CharField(max_length=255, unique=True, editable=False)

    def __str__(self):
        return f"{self.Firstname} {self.Surname}"

    def save(self, *args, **kwargs):
        # Auto-generate username before saving
        self.Username = f"{self.Firstname}{self.Surname}".lower()
        super().save(*args, **kwargs)


# Class Model
class Class(models.Model):
    ClassID = models.AutoField(primary_key=True)
    ClassName = models.CharField(max_length=100)
    LecturerID = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    SessionNumber = models.IntegerField(default=0)

    def __str__(self):
        return self.ClassName


# Enrollment Model (Explicit Student-Class Relationship)
class Enrollment(models.Model):
    EnrollmentID = models.AutoField(primary_key=True)
    StudentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    ClassID = models.ForeignKey(Class, on_delete=models.CASCADE)
    EnrollmentDate = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.StudentID.Firstname} enrolled in {self.ClassID.ClassName}"


# Attendance Record Model
class AttendanceRecord(models.Model):
    AttendanceID = models.AutoField(primary_key=True)
    Date = models.DateField()
    Time = models.TimeField()
    EnrollmentID = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    AttendanceStatus = models.CharField(
        max_length=8,
        choices=[('Present', 'Present'), ('Absent', 'Absent')]
    )

    def __str__(self):
        return f"{self.EnrollmentID} - {self.AttendanceStatus}"


# Grade Model
class Grade(models.Model):
    GradeID = models.AutoField(primary_key=True)
    EnrollmentID = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    FinalGrade = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return f"Grade {self.FinalGrade} for {self.EnrollmentID.StudentID.Firstname} in {self.EnrollmentID.ClassID.ClassName}"
