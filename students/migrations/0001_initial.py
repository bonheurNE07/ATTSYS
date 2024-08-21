# Generated by Django 3.0.7 on 2024-08-19 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0002_auto_20240818_2355'),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_date', models.DateField(auto_now_add=True)),
                ('completion_status', models.CharField(choices=[('ongoing', 'Ongoing'), ('completed', 'Completed')], max_length=20)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Student')),
            ],
        ),
    ]
