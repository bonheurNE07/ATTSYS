from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('enrollments/', views.enrollment_list, name='enrollment_list'),
    path('enrollments/add/', views.add_enrollment, name='add_enrollment'),
    path('enrollments/edit/<int:enrollment_id>/', views.edit_enrollment, name='edit_enrollment'),
    path('enrollments/delete/<int:enrollment_id>/', views.delete_enrollment, name='delete_enrollment'),
    path('enrollments/student/<int:student_id>/', views.student_enrollment_detail, name='student_enrollment_detail'),
]
