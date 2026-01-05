from django.contrib import admin
from .models import CustomUser, Student, Room, Complaint, FeePayment

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Room)
admin.site.register(Complaint)
admin.site.register(FeePayment)
