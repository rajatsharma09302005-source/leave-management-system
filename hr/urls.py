from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'hr'

urlpatterns = [
    path('employees/update/<int:id>/', views.update_employee, name='update_employee'),
    path('employees/delete/<int:id>/', views.delete_employee, name='delete_employee'),
    path("login/", views.hr_login, name="hr_login"),
    path("logout/", views.hr_logout, name="hr_logout"),
    path("employee/", views.employee_list, name="employee_list"),
    path("employee/add/", views.add_employee, name="add_employee"),
    path('', views.hr_dashboard, name='hr_dashboard'),
    path('leave-requests/', views.leave_requests, name='leave_requests'),
    path("approve/<int:leave_id>/", views.approve_leave, name="approve_leave"),
    path("reject/<int:leave_id>/", views.reject_leave, name="reject_leave"),
]