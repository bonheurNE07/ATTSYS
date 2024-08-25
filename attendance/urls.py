from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='attendance_list'),
    path('record/', views.record_attendance, name='record_attendance'),
    path('manual/', views.manual_attendance, name='manual_attendance'),
    path('detail/<int:student_id>/', views.attendance_detail, name='attendance_detail'),
    path('report/', views.attendance_report, name='attendance_report'),
]
