# Generated by Django 5.1.4 on 2025-01-05 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0002_attendancerecord_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancerecord',
            name='AttendanceStatus',
            field=models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], default='Absent', max_length=8),
        ),
    ]
