from django.core.management.base import BaseCommand
from hostelapp.models import Room

class Command(BaseCommand):
    help = 'Create 67 rooms with fixed capacity of 3 students each'

    def handle(self, *args, **kwargs):
        Room.objects.all().delete()  # Optional: delete previous rooms

        total_rooms = 67
        for i in range(1, total_rooms + 1):
            room_number = f"{100 + i}"  # Room numbers like 101, 102, ...
            Room.objects.create(room_number=room_number, max_capacity=3)

        self.stdout.write(self.style.SUCCESS(f"✅ Created {total_rooms} rooms, each with capacity 3 (Total capacity: {total_rooms * 3})"))
