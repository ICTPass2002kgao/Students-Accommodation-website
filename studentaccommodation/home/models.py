import uuid
from django.db import models
from django.contrib.auth.models import User  
 
class Accommodation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accommodation_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    email = models.EmailField(default='maphilegman@gmail.com')
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=13)  
    logo = models.ImageField(upload_to="landlord_logos/", null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.accommodation_name
class AccommodationImage(models.Model):
    accommodation = models.ForeignKey(
        Accommodation, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="accommodation_images/")

    def __str__(self):
        return f"Image for {self.accommodation.accommodation_name}"
 

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    email = models.EmailField(unique=True, verbose_name="Email")
    cell_phone = models.CharField(max_length=15)
    gender = models.CharField(
        max_length=6, 
    )
    enrolled_university = models.CharField(
        max_length=50, 
    )
    bursary = models.CharField(
        max_length=50, 
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} {self.surname}"

class Application(models.Model):
    applied_at = models.DateTimeField(auto_now_add=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, null=True) 
    status = models.CharField(
        max_length=10,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
    )

    def __str__(self):
        return f"Application by {self.student.name} at {self.accommodation.accommodation_name}"
