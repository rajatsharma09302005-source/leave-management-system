
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from employee.models import LeaveRequest
from django.contrib.auth.models import User
from datetime import date

# HR check
def is_hr(user):
    return user.is_staff

# def hr_dashboard(request):
#     total_employees = User.objects.filter(is_staff=False).count()  # count all employees, not HR
#     pending_requests = LeaveRequest.objects.filter(status='pending').count()
#     approved_today = LeaveRequest.objects.filter(
#         status='Approved',
#         submitted_at__date=date.today()
#     ).count()

#     context = {
#         'total_employees': total_employees,
#         'pending_requests': pending_requests,
#         'approved_today': approved_today
#     }
#     return render(request, 'hr/hr_dashboard.html', context)



from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.timezone import now
from employee.models import LeaveRequest


@login_required(login_url='/hr/login/')
@user_passes_test(is_hr)
def hr_dashboard(request):

    # total employees (excluding HR/admin)
    total_employees = User.objects.filter(is_staff=False).count()

    # leave statistics
    pending_requests = LeaveRequest.objects.filter(status="Pending").count()
    approved_requests = LeaveRequest.objects.filter(status="Approved").count()
    rejected_requests = LeaveRequest.objects.filter(status="Rejected").count()

    # approved today
    today = now().date()
    approved_today = LeaveRequest.objects.filter(
        status="Approved",
        submitted_at__date=date.today()
    ).count()

    context = {
        "total_employees": total_employees,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "rejected_requests": rejected_requests,
        "approved_today": approved_today,
    }

    return render(request, "hr/hr_dashboard.html", context)





@login_required(login_url='/hr/login/')
@user_passes_test(is_hr)
def leave_requests(request):
    # HR should see ALL leave requests, not only their own
    leaves = LeaveRequest.objects.all().order_by('-submitted_at')

    return render(request, "hr/leave_requests.html", {
        'leaves': leaves
    })
    
    
    



from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from employee.models import LeaveRequest, LeaveBalance
from django.conf import settings
from django.core.mail import send_mail

@login_required(login_url='/hr/login/')
@user_passes_test(is_hr)
def approve_leave(request, leave_id):
    if request.method=='POST':    
        leave = get_object_or_404(LeaveRequest, id=leave_id)

        if leave.status == "pending":  # prevent double approval
            leave.status = "approved"
            leave.save()
            
            employee_email = leave.employee.email

            send_mail(
                subject="Leave Request Approved",
                message=f"""
        Hello {leave.employee.username},

        Your leave request from {leave.start_date} to {leave.end_date} has been APPROVED.

        Thank you.
        HR Department
        """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[employee_email],
                fail_silently=False,
            )

    

            # Update leave balance
            balance, created = LeaveBalance.objects.get_or_create(employee=leave.employee)
            days = leave.total_days  # access property without parentheses
            balance.used_leaves += days
            balance.save()
            
            

        return redirect('hr:leave_requests')



@login_required(login_url='/hr/login/')
@user_passes_test(is_hr)
def reject_leave(request, leave_id):
    if request.method == "POST":
        leave = get_object_or_404(LeaveRequest, id=leave_id)
        if leave.status == "pending":
            leave.status = "rejected"
            leave.save()
            
            
            employee_email = leave.employee.email

            send_mail(
                subject="Leave Request Approved",
                message=f"""
        Hello {leave.employee.username},

        Your leave request from {leave.start_date} to {leave.end_date} has been Rejected.

        Thank you.
        HR Department
        """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[employee_email],
                fail_silently=False,
            )

            
    return redirect("hr:leave_requests")




from django.contrib.auth import authenticate, login , logout
from django.shortcuts import render, redirect

def hr_login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("hr:hr_dashboard")

        return render(request, "hr/login.html", {"error":"Invalid HR credentials"})

    return render(request, "hr/login.html")


def hr_logout(request):
    logout(request)
    return redirect('hr:hr_login')







from django.db.models import Q


@login_required
@user_passes_test(is_hr)
def employee_list(request):
    search_query = request.GET.get('search', '')
    # it is ued to get data from url that show using get form method

    # Filter employees based on search
    if search_query:
        employees = User.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query),
            is_staff=False
        )
    else:
        employees = User.objects.filter(is_staff=False)

    employee_data = []

    for emp in employees:
        balance, created = LeaveBalance.objects.get_or_create(employee=emp)

        employee_data.append({
            'id': emp.id,
            'name': emp.username,
            'email': emp.email,
            'total_leaves': balance.total_leaves,
            'used_leaves': balance.used_leaves,
            'remaining_leaves': balance.remaining_leaves
        })

    return render(request, 'hr/employee_list.html', {
        'employee_data': employee_data,
        'search_query': search_query
    })






from django.contrib import messages
user_passes_test

# HR check
def is_hr(user):
    return user.is_staff

@login_required
@user_passes_test(is_hr)
def add_employee(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    is_staff=False  # regular employee
                )
                messages.success(request, f"Employee {username} created successfully!")
                return redirect('hr:employee_list')
        else:
            messages.error(request, "All fields are required!")

    return render(request, 'hr/add_employee.html')
    




@login_required
@user_passes_test(is_hr)
def update_employee(request, id):
    emp = User.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if username and email:
            emp.username = username
            emp.email = email
            emp.save()
            messages.success(request, "Employee updated successfully!")
            return redirect('hr:employee_list')
        else:
            messages.error(request, "All fields are required!")

    return render(request, 'hr/update_employee.html', {'employee': emp})




@login_required
@user_passes_test(is_hr)
def delete_employee(request, id):
    emp = User.objects.get(id=id)
    emp.delete()
    messages.success(request, "Employee deleted successfully!")
    return redirect('hr:employee_list')





