from django.db import models
from django.contrib.auth.models import User

class LeaveRequest(models.Model):
    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,        # TEMPORARY
        blank=True        # TEMPORARY
    )

    

    start_date = models.DateField()
    end_date = models.DateField()

    leave_type = models.CharField(max_length=30)
    message = models.TextField(max_length=250)

    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"{self.employee.username} ({self.start_date})"
    
    
    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1
    
    
    
class LeaveBalance(models.Model):

    employee = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    total_leaves = models.IntegerField(default=20)
    used_leaves = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.employee.username} Leave Balance"

    @property
    def remaining_leaves(self):
        return self.total_leaves - self.used_leaves