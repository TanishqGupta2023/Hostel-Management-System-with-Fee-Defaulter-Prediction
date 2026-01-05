from hostelapp.models import CustomUser
from django.contrib.auth.hashers import make_password

admin = CustomUser.objects.create(
    username='admin',
    email='admin@example.com',
    password=make_password('admin123'),
    role='admin',
    is_superuser=True,
    is_staff=True
)
admin.save()
