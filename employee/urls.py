from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "employee"

urlpatterns = [
    path('leave/delete/<int:id>/', views.delete_leave, name='delete_leave'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.employee_dashboard, name='employee_dashboard'),
    path('apply-leave/', views.apply_leave, name='apply_leave'),
    path('leave-requests/', views.leave_requests, name='leave_requests'),
    path("my_profile/", views.my_profile, name="my_profile")
]