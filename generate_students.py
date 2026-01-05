import os
import django
import random
from django.contrib.auth.hashers import make_password


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostelml.settings")
django.setup()

from hostelapp.models import CustomUser, Student, FeePayment


departments = ['CSE', 'ECE', 'ME']
years = [2022, 2023, 2024]

created = 0

for i in range(1, 201): 
    username = f'student{i}'
    email = f'student{i}@example.com'
    if CustomUser.objects.filter(username=username).exists():
        continue  
    password = make_password('password123')
    
    attendance = random.randint(40, 100)
    internal_score = random.randint(30, 100)
    parent_income = random.randint(50000, 200000)
    cgpa = round(random.uniform(5.0, 10.0), 2)
    scholarship = random.choice([0, 1])
    
   
    fee_paid = attendance > 70 and internal_score > 60 and parent_income > 80000
    
    contact = str(random.choice([6,7,8,9])) + ''.join([str(random.randint(0,9)) for _ in range(9)])

    user = CustomUser.objects.create(username=username, email=email, password=password, role='student')

    student = Student.objects.create(
        user=user,
        contact_number=contact,
        address="City X",
        department=random.choice(departments),
        year=random.choice(years),
        attendance_percent=attendance,
        internal_score=internal_score,
        parent_income=parent_income,
        cgpa=cgpa,
        scholarship=scholarship,
        payment_status='paid' if fee_paid else 'unpaid',
        roll_number=f'RN{i:03}',
        has_paid_fees=fee_paid
    )

    FeePayment.objects.create(
        student=student,
        fee_paid=fee_paid
    )
    
    created += 1

print(f"✅ {created} new students created with correct FeePayment records.")
