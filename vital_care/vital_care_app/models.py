from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone



class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length = 60)
    is_doctor = models.BooleanField(default = False)
    is_patient = models.BooleanField(default = False)
    role = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/', default = None)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

class Patient(models.Model):
    email = models.EmailField(max_length=80)
    user  = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length = 6)
    phone_number = models.CharField(max_length=10)
    height = models.CharField(max_length=5)
    weight = models.CharField(max_length=5)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=5)
    medical_history = models.CharField(max_length=255)
    date_of_birth = models.CharField(max_length=20)
    address = models.CharField(max_length =255)
    
class Specialist(models.Model):
    specialist_name = models.CharField(max_length = 50)
    
    
class Blood_group(models.Model):
    blood_group = models.CharField(max_length=5)

class Gender(models.Model):
    gender = models.CharField(max_length=10)

    
    
class Doctor(models.Model):
    email = models.EmailField(max_length=80)
    user  = models.OneToOneField(User,on_delete=models.SET_NULL,null=True)
    spec = models.ForeignKey(Specialist,on_delete=models.SET_NULL,null=True)
    first_name = models.CharField(max_length=80)
    age = models.IntegerField()
    last_name = models.CharField(max_length = 60)
    phone_number = models.CharField(max_length=10)
    gender= models.CharField(max_length =10)
    specialist = models.CharField(max_length=255)
    experience = models.CharField(max_length=3)
    qualification = models.CharField(max_length=30)
    consultation_fee = models.CharField(max_length =5)
    

class Portal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length =255)
    
class Portal_items(models.Model):
    user_type = models.CharField(max_length=255)
    name = models.ForeignKey(Portal,on_delete=models.SET_NULL,null=True)
    title =models.CharField(max_length=100)
    url =models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    order = models.IntegerField()
    
class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null =True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=80)
    patientID = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    height = models.CharField(max_length=4)
    weight = models.CharField(max_length=4)
    age = models.CharField(max_length=3)
    preferred_date =models.CharField(max_length=10)
    symptoms = models.CharField( max_length=255,null = True)
    blood_group = models.CharField(max_length=3)
    doctor_selected = models.CharField(max_length =50)
    speciality = models.CharField(max_length=30)
    reason = models.CharField(max_length=255) 
    is_approved_recep = models.BooleanField(default=False)
    is_approved_doc = models.BooleanField(default=False)
    amount_to_be_paid = models.CharField(max_length=5)
    remark = models.CharField(max_length=500,null = True)
    visited = models.BooleanField(default =False)
    visited_doc = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=50,default="Pending")
    is_prescribed = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default =False)
    
    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    instruction = models.CharField(max_length=255)
    medicine = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    days= models.CharField(max_length=255)
    diagnosis = models.CharField(max_length=255)
    # date = models.DateTimeField(default = timezone.now)
    
    
    

        