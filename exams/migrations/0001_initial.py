# Generated by Django 3.0.7 on 2024-08-18 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('courses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.DurationField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='ExamAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Present'), ('A', 'Absent')], max_length=1)),
                ('rfid_card', models.CharField(max_length=20)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.Exam')),
                ('recorded_by', models.ForeignKey(limit_choices_to={'usertype': 4}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Student')),
            ],
            options={
                'unique_together': {('student', 'exam')},
            },
        ),
    ]
