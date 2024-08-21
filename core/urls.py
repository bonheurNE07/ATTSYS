from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register-employee/', views.registration_employee, name='register_employee'),

    path('students/create/', views.create_student, name='create_student'),
    path('students/update/<int:pk>/', views.update_student, name='update_student'),
    path('students/delete/<int:pk>/', views.delete_student, name='delete_student'),

    path('employees/create/', views.create_employee, name='create_employee'),
    path('employees/update/<int:pk>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:pk>/', views.delet_employee, name='delete_employee'),

    path('rfid/assign/', views.assign_rfid, name='assign_rfid'),
    path('rfid/update/<int:pk>/', views.update_rfid, name='update_rfid'),
    path('rfid/delete/<int:pk>/', views.delete_rfid, name='delete_rfid'),
]