from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

# Custom User Model for Role-Based Authentication
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('housekeeper', 'Housekeeper'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username

# Hostel Model
class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    has_blocks = models.BooleanField(default=False)  # True if hostel has blocks
    has_wings = models.BooleanField(default=False)   # True if hostel has wings

    def __str__(self):
        return self.name

# Block Model (for hostels with blocks)
class Block(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="blocks")
    name = models.CharField(max_length=50)  # e.g., "Block A"

    class Meta:
        unique_together = ('hostel', 'name')  # Ensures unique block names within a hostel

    def __str__(self):
        return f"{self.hostel.name} - {self.name}"

# Wing Model (for hostels with wings)
class Wing(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="wings")
    name = models.CharField(max_length=50)  # e.g., "Western Wing"

    class Meta:
        unique_together = ('hostel', 'name')  # Ensures unique wing names within a hostel

    def __str__(self):
        return f"{self.hostel.name} - {self.name}"

# Room Model
class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single Room'),
        ('double', 'Double Room'),
        ('triple', 'Triple Room'),
        ('quad', 'Quad Room'),
    )
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True, related_name="rooms")
    wing = models.ForeignKey(Wing, on_delete=models.SET_NULL, null=True, blank=True, related_name="rooms")
    number = models.CharField(max_length=10)
    capacity = models.IntegerField()
    occupied = models.IntegerField(default=0)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)

    class Meta:
        unique_together = ('hostel', 'number')  # Ensures unique room numbers within a hostel

    def clean(self):
        # Validate that occupied rooms do not exceed capacity
        if self.occupied > self.capacity:
            raise ValidationError("Occupied rooms cannot exceed capacity")

    def save(self, *args, **kwargs):
        self.clean()  # Run validation before saving
        super().save(*args, **kwargs)

    def __str__(self):
        location = self.block.name if self.block else (self.wing.name if self.wing else self.hostel.name)
        return f"{location} - Room {self.number} ({self.room_type})"

# Student Model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    registration_number = models.CharField(max_length=20, unique=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.registration_number}"

# Housekeeper Model
class Housekeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='housekeeper')
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="housekeepers")
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True, blank=True, related_name="housekeepers")
    wing = models.ForeignKey(Wing, on_delete=models.SET_NULL, null=True, blank=True, related_name="housekeepers")

    def __str__(self):
        location = self.block.name if self.block else self.wing.name if self.wing else self.hostel.name
        return f"{self.user.username} - {location} Housekeeper"

# Check-in Model
class CheckIn(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='checkins')  # Link to Student model
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='checkins')
    checked_in = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.room.number} - {'Checked In' if self.checked_in else 'Pending'}"

# Complaint Model
class Complaint(models.Model):
    PENDING = 'pending'
    RESOLVED = 'resolved'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (RESOLVED, 'Resolved')
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.status}"

# Emergency Model
class Emergency(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emergencies')
    emergency_type = models.CharField(max_length=50)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Emergency: {self.emergency_type} by {self.student.username}"