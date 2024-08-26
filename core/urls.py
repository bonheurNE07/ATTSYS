from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication and Registration URLs
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/employee/', views.registration_employee, name='register_employee'),

    # Student Management URLs
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.create_student, name='create_student'),
    path('students/update/<int:pk>/', views.update_student, name='update_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    # Employee Management URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/update/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', views.delete_employee, name='delete_employee'),

    # RFID Card Management URLs
    path('rfid/', views.rfid_list, name='rfid_list'),
    path('rfid/assign/', views.assign_rfid, name='assign_rfid'),
    path('rfid/update/<int:pk>/', views.update_rfid, name='update_rfid'),
    path('rfid/delete/<int:pk>/', views.delete_rfid, name='delete_rfid'),

    # Dashboard URLs
    path('hod_dashboard/', views.hod_dashboard, name='hod_dashboard'),
    path('lecturer_dashboard/', views.lecturer_dashboard, name='lecturer_dashboard'),

    # Home URL
    path('', views.home, name='home'),
]
