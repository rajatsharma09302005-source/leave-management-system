from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import LeaveRequest
from django.conf import settings
from django.core.mail import send_mail



from django.contrib.auth.decorators import login_required
from django.db.models import Count



@login_required
def employee_dashboard(request):
    """
    This view renders the dashboard (base.html).
    By default, it can show the Apply Leave section.
    """
    leave_requests = LeaveRequest.objects.all().order_by('-submitted_at')
    return render(request, 'employee/home.html', {
        'leave_requests': leave_requests
    })







from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .models import LeaveRequest

@login_required
def apply_leave(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        leave_type = request.POST.get('leave_type')
        message = request.POST.get('message')

        # Validation
        if start_date and end_date and leave_type and message:
            leave = LeaveRequest.objects.create(
                employee=request.user,   # ✅ LINK TO LOGGED-IN USER
                
                start_date=start_date,
                end_date=end_date,
                leave_type=leave_type,
                message=message
            )

            # Email to HR
            subject = "New Leave Request Submitted"
            email_message = (
                f"Employee: {leave.employee}\n"
                f"From: {start_date}\n"
                f"To: {end_date}\n"
                f"Leave Type: {leave_type}\n"
                f"Reason: {message}\n\n"
                f"Admin panel: http://127.0.0.1:8000/admin/"
            )

            send_mail(
                subject,
                email_message,
                settings.EMAIL_HOST_USER,
                ['rajatsharmafact@gmail.com'],
                fail_silently=False,
            )

            return redirect('employee:leave_requests')

        return render(request, 'employee/apply_leave.html', {
            'error': 'All fields are required'
        })

    return render(request, 'employee/apply_leave.html')


# @login_required
# def apply_leave(request):
#     """
#     Handles the Apply Leave form (HTML form submission).
#     """
#     if request.method == 'POST':
#         employee_name = request.POST.get('employee_name')
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         leave_type = request.POST.get('leave_type')
#         message = request.POST.get('message')

#         # Simple validation
#         if employee_name and start_date and end_date and leave_type and message:
#             LeaveRequest.objects.create(
#                 employee_name=employee_name,
#                 start_date=start_date,
#                 end_date=end_date,
#                 leave_type=leave_type,
#                 message=message
#             )
            
#             subject="this is employee leave request"
#             message=f"hyy i am {employee_name} this a leave request from {start_date} to {end_date} for {leave_type} due to {message}\n click here to go admin page http://127.0.0.1:8000/leave-requests/"
#             from_email=settings.EMAIL_HOST_USER
#             recipient_list=['rajatsharmafact@gmail.com']
#             send_mail(subject,message,from_email,recipient_list)
            
#             return redirect('employee:leave_requests')

#         # If validation fails
#         return render(request, 'apply_leave.html', {
#             'error': 'All fields are required'
#         })

#     return render(request, 'apply_leave.html')

# @login_required
# def leave_requests(request):
#     """
#     Displays the leave request table.
#     """
#     leave_requests = LeaveRequest.objects.all().order_by('-submitted_at')
#     return render(request, 'leave_requests.html', {
#         'leave_requests': leave_requests
#     })
    
@login_required
def leave_requests(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, 'employee/leave_requests.html', {
        'leave_requests': leaves
    })
    


from django.shortcuts import get_object_or_404, redirect


@login_required
def delete_leave(request, id):
    if request.method == "POST":
        leave = get_object_or_404(LeaveRequest, id=id)

        # Only allow deletion if pending
        if leave.status == "pending":
            leave.delete()
        
        return redirect('employee:leave_requests')
    else:
        # If someone tries GET, redirect to leave requests
        return redirect('employee:leave_requests')
    
    
    


# @login_required
# def my_profile(request):
#     user = request.user

#     TOTAL_LEAVES = 20

#     approved_leaves = LeaveRequest.objects.filter(
#         employee_name=user.username,
#         status="approved"
#     ).count()

#     # Calculate total used days
#     leaves_used = 0
#     for leave in approved_leaves:
#         leaves_used += (leave.end_date - leave.start_date).days + 1  # +1 to include both start and end dates

#     remaining_leaves = TOTAL_LEAVES - leaves_used
#     if remaining_leaves < 0:
#         remaining_leaves = 0  # Prevent negative leaves

#     context = {
#         "user": user,
#         "total_leaves": TOTAL_LEAVES,
#         "used_leaves": leaves_used,
#         "remaining_leaves": remaining_leaves,
#     }

#     return render(request, "my_profile.html", context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employee.models import LeaveRequest

@login_required
def my_profile(request):
    total_leaves = 20  # yearly quota

    # ✅ ONLY approved leaves
    approved_leaves = LeaveRequest.objects.filter(
        employee=request.user,
        status='Approved'
    )

    leaves_used = 0
    for leave in approved_leaves:
        days = (leave.end_date - leave.start_date).days + 1
        leaves_used += days

    remaining_leaves = max(total_leaves - leaves_used, 0)

    context = {
        'total_leaves': total_leaves,
        'leaves_used': leaves_used,
        'remaining_leaves': remaining_leaves,
    }

    return render(request, 'employee/my_profile.html', context)










# employee/views.py

from django.contrib.auth import authenticate, login ,logout
from django.shortcuts import render, redirect

def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_staff:
            login(request, user)
            return redirect("employee:employee_dashboard")

        return render(request, "employee/login.html", {"error":"Invalid credentials"})

    return render(request, "employee/login.html")

    
def logout_view(request):
    logout(request)
    return redirect('employee:login')