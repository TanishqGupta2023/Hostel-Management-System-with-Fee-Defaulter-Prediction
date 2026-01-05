import os
import django
import random
from django.db import transaction


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hostelml.settings")
django.setup()

from hostelapp.models import Student, FeePayment


students = list(Student.objects.all())
random.shuffle(students)


paid_students = students[:70]
unpaid_students = students[70:]

paid_count = 0
unpaid_count = 0

with transaction.atomic():
    for student in paid_students:
        student.has_paid_fees = True
        student.payment_status = 'paid'
        student.save()

        fee, _ = FeePayment.objects.get_or_create(student=student)
        fee.fee_paid = True
        fee.save()
        paid_count += 1

    for student in unpaid_students:
        student.has_paid_fees = False
        student.payment_status = 'unpaid'
        student.save()

        fee, _ = FeePayment.objects.get_or_create(student=student)
        fee.fee_paid = False
        fee.save()
        unpaid_count += 1

print(f"✅ Updated {paid_count} students as PAID.")
print(f"✅ Updated {unpaid_count} students as UNPAID.")
