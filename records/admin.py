from django.contrib import admin
from .models import Lecturer, Student, Class, AttendanceRecord, Grade, Enrollment

admin.site.register(Lecturer)
admin.site.register(Student)
admin.site.register(Class)
admin.site.register(AttendanceRecord)
admin.site.register(Grade)
admin.site.register(Enrollment)
