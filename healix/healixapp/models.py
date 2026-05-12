from django.db import models
class SuperAdmin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # plain text for now
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default='superadmin')

class OldAgeHome(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone_number=models.CharField(max_length=15)
    place=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class Admin(models.Model):
    superadmin = models.ForeignKey(SuperAdmin, on_delete=models.CASCADE)
    home = models.ForeignKey(OldAgeHome, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default='admin')


from django.db import models
class Nurse(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  
    home = models.ForeignKey('OldAgeHome', on_delete=models.CASCADE)  # many nurses per home
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default='nurse')



from django.db import models

class Doctor(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)  
    home = models.ForeignKey('OldAgeHome', on_delete=models.CASCADE)  # many doctors per home
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=50, default='doctor')

    def __str__(self):
        return f"{self.name} ({self.specialization}) - {self.home.name}"




from django.db import models

class Resident(models.Model):
    home = models.ForeignKey('OldAgeHome', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender_choices = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
    gender = models.CharField(max_length=10, choices=gender_choices)
    room_number = models.CharField(max_length=10, null=True, blank=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=10)
    emergency_address = models.TextField(null=True, blank=True)
    emergency_place = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.home.name}"


class Vitals(models.Model):
    nurse = models.ForeignKey(Nurse, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    blood_pressure = models.CharField(max_length=10, default="")
  # e.g., "120/80"
    blood_sugar = models.FloatField()  # mg/dL
    heart_rate = models.PositiveIntegerField()  # bpm
    oxygen_level = models.FloatField()  # percentage instead of body temperature
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident.name} - {self.nurse.name} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
# models.py
from django.db import models
from .models import Resident

class Prescription(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    additional_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} for {self.resident.name}"


