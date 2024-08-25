from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    path('exam-list/', views.exam_list, name='exam_list'),
    path('exam-add/', views.add_exam, name='add_exam'),
    path('exam-update/<int:exam_id>/', views.update_exam, name='update_exam'),
    path('exam-delete/<int:exam_id>/', views.delete_exam, name='delete_exam'),

    path('attendance-list/', views.exam_attendance_list, name='exam_attendance_list'),
    path('attendance-add/', views.add_exam_attendance, name='add_exam_attendance'),
    path('attendance-update/<int:attendance_id>/', views.update_exam_attendance, name='update_exam_attendance'),
    path('attendance-delete/<int:attendance_id>/', views.delete_exam_attendance, name='delete_exam_attendance'),
]
