from django.db import models
from django.contrib.auth.models import AbstractUser


# 🔹 Custom User with Role (Admin / Student)
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


# 🔹 Room Model
class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    max_capacity = models.IntegerField(default=3)

    def __str__(self):
        return f"Room {self.room_number}"

    def current_occupants(self):
        return Student.objects.filter(room=self).count()

    def is_full(self):
        return self.current_occupants() >= self.max_capacity


# 🔹 Student Model (linked to CustomUser)
class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=10)
    address = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    payment_status = models.CharField(max_length=20, default='unpaid')
    roll_number = models.CharField(max_length=20) 
    department = models.CharField(max_length=100)  
    year = models.IntegerField(null=True, blank=True)  
    attendance_percent = models.IntegerField(default=0)
    internal_score = models.IntegerField(default=0)
    parent_income = models.IntegerField(default=0)
    scholarship = models.BooleanField(default=False)
    hostel_stay = models.BooleanField(default=True)
    cgpa = models.FloatField(null=True, blank=True)
    previous_default = models.IntegerField(null=True, blank=True)
    has_paid_fees = models.BooleanField(default=False)
    fee_receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    is_predicted_defaulter = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username


# 🔹 Complaint Model
class Complaint(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    admin_reply = models.TextField(blank=True)
    STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('resolved', 'Resolved'),
]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
  

    def __str__(self):
        return f"{self.category} - {self.student.user.username}"




# 🔹 Fee Payment Model
class FeePayment(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    fee_paid = models.BooleanField(default=False)
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)

    def __str__(self):
        return f"FeePayment: {self.student.user.username} - {'Paid' if self.fee_paid else 'Unpaid'}"