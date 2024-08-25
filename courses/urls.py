from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),  # URL for listing all courses
    path('<int:course_id>/', views.course_detail, name='course_detail'),  # URL for viewing a specific course
    path('create/', views.course_create, name='course_create'),  # URL for creating a new course
    path('<int:course_id>/edit/', views.course_update, name='course_update'),  # URL for updating an existing course
    path('<int:course_id>/delete/', views.course_delete, name='course_delete'),  # URL for deleting a course
]
