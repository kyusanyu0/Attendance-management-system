from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employer', '雇用主'),
        ('employee', '従業員'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    employment_type = models.CharField(max_length=10, choices=[('fulltime', '社員'), ('parttime', 'AP')])

class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    break_start = models.DateTimeField(null=True)
    break_end = models.DateTimeField(null=True)
    date = models.DateField(auto_now_add=True)

