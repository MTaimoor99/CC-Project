from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .forms import User

# Create your models here.

class AttendanceRecord(models.Model):
      user=models.ForeignKey(User, on_delete=models.CASCADE)
      timestamp=models.DateTimeField(auto_now_add=True)
      attendance_date=models.DateField()