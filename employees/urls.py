from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('add/', views.add_employee, name='add_employee'),
    path('<int:pk>/update/', views.update_employee, name='update_employee'),
    path('<int:pk>/delete/', views.delete_employee, name='delete_employee'),
]
