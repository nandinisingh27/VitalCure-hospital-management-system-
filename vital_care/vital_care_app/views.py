from django.shortcuts import render
import re
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Doctor
from .models import Patient
from .models import Portal
from .models import Specialist
from .models import Portal_items
from .models import Appointment



def patient_register(request):
    if request.method == "POST":
        data = json.loads(request.body)
        first_name = data.get('first_name')
        if first_name is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                return JsonResponse({'error':'Please enter a valid first name'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid first name'},status =400)
        
        last_name = data.get('last_name')
        
        
        email = data.get('email')
        if email is not None:
            if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                return JsonResponse({'error':'Please enter a valid email'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid email ID'},status =400)
        
        phone_number = data.get('phone_number')
        if phone_number is not None:
            if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        
        height = str(data.get('height'))
        if height is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",height)):
                return JsonResponse({'error':'Please enter valid height'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid height'},status =400)
        
        weight = str(data.get('weight'))
        if weight is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",weight)):
                return JsonResponse({'error':'Please enter valid weight'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid weight'},status =400)
        
        age = str(data.get('age'))
        if age is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",age)):
                return JsonResponse({'error':'Please enter valid age'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid age'},status =400)
        
        gender = data.get('gender')
        if gender is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",gender)):
                return JsonResponse({'error':'Please enter valid gender'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid gender'},status =400)
        
        
        blood_group = data.get('blood_group')
        if blood_group is not None:
            if not bool(re.match(r"^(A|B|AB|O)[+-]$",blood_group)):
                return JsonResponse({'error':'Please enter valid blood group'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid blood group'},status =400)
        
        medical_history = data.get('medical_history')
        
        
        date_of_birth = data.get('date_of_birth')
        if date_of_birth is  None:
            return JsonResponse({'error':'Please enter valid date of birth'},status =400)

        
        address = data.get('address')
        if address is None:
            return JsonResponse({'error':'Please enter a valid address '} ,status =400)
        password = data.get('password')
        cpassword =  data.get('cpassword')
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
            return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):
            return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'error': 'User already exists!!,please try with another email address'},status=400)
        

        user = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,role = "Patient",is_doctor=0,is_patient=1,password=password)
        Patient.objects.create(user =user,email =email,first_name = first_name,last_name = last_name,phone_number= phone_number,height = height,weight =weight,age =age,gender = gender,blood_group = blood_group,medical_history = medical_history,date_of_birth=date_of_birth,address=address)
        send_mail(
            " Account created",
            "Your VITALCURE patient account has been successfully created!!",
            "nandinisingh52891@gmail.com",
            [email],
            fail_silently=False
        )
        
        return JsonResponse({'message':'Patient Account created successfully!!'},status = 201)

    else:
        return JsonResponse({'error':'Invalid method'},status =405)
    
    
def doctor_register(request):
    if request.method=="POST":
        data = json.loads(request.body)
        first_name = data.get('first_name')
        if first_name is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                return JsonResponse({'error':'Please enter a valid first name'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid first name'},status =400)
        
        last_name = data.get('last_name')
        
        
        email = data.get('email')
        if email is not None:
            if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                return JsonResponse({'error':'Please enter a valid email'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid email ID'},status =400)
        age = str(data.get('age'))
        if age is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",age)):
                return JsonResponse({'error':'Please enter valid age'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid age'},status =400)
        
        phone_number = data.get('phone_number')
        if phone_number is not None:
            if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        gender = data.get('gender')
        if gender is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",gender)):
                return JsonResponse({'error':'Please enter valid gender'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid gender'},status =400)
        specialist = data.get('specialist')
        if specialist is None:
            return JsonResponse({'error':'Please a enter valid speciality'},status =400)
        qualification = data.get('qualification')
        if qualification is None:
            return JsonResponse({'error':'Please a enter valid qualification'},status =400)
        consultation_fee = str(data.get('consultation_fee'))
        if consultation_fee is not None:
            if not bool(re.match(r"^[0-9]*$",consultation_fee)):
                return JsonResponse({'error':'Please enter a valid consultation fee'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid consultation fee'},status =400)
        experience=data.get('experience')
        password = data.get('password')
        cpassword =  data.get('cpassword')
        speacialist_id = Specialist.objects.filter(specialist_name =specialist).values()
        spec_id = speacialist_id[0]['id']
        print(spec_id)
        

        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
        
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'error': 'User already exists!!,please try with another email address'},status=400)
        user  = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,role = "Doctor",is_doctor=1,is_patient=0,password=password )
        Doctor.objects.create(user = user ,spec_id = spec_id,email =email,first_name = first_name,last_name = last_name,phone_number= phone_number,age=age,gender = gender,specialist=specialist,experience =experience,qualification=qualification,consultation_fee = consultation_fee)
        send_mail(
            " Account created",
            "Your VITALCURE doctor account has been successfully created!!",
            "nandinisingh52891@gmail.com",
            [email],
            fail_silently=False
        )
        return JsonResponse({'message':'Doctor account created successfully'},status =201)

def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        email = data.get('email')
        password = data.get('password')
        if email is None:
            return JsonResponse({'error': 'Please enter email'}, status=400)
        if password is None:
            return JsonResponse({'error': 'Please enter password'}, status=400)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            role = user.role
            return JsonResponse({'message':f'{role} successfully logged in',  'route': role}, status=200)

        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    else:
        return JsonResponse({'error': 'Invalid method'}, status=405)
    
    
def logout_user(request):
    if request.method == "GET":
        user  = request.user
        if user.is_authenticated:
            logout(request)
            return JsonResponse({'message':'Logged out!!'},status = 200)
        else:
            return JsonResponse({'error':'Invalid user'},status = 400)
        
    else:
        return JsonResponse({'error':'Invalid method'},status =405 )
        
def side_menu(request):
    if request.method=="GET":
        user = request.user
        data = User.objects.filter(email=user).values()
        role = data[0]['role']
        first_name = data[0]['first_name']
        last_name = data[0]['last_name']
        name = first_name+ " " + last_name
        if role == "Doctor":
            doc_data = Doctor.objects.filter(email = user).values()
            speciality = doc_data[0]['specialist']
            details =[]
            val = {
                'name':"Dr. "+name,
                'speciality':speciality,
                'first_name':"Dr. "+first_name,
                
                }
            details.append(val)
            item = Portal_items.objects.filter(user_type = role).values().order_by('order')
            final_item=[]
            for info in item:
                value = {
                    'title':info['title'],
                    'icon':info['icon'],
                    'url':info['url']
                    }
                final_item.append(value)

            return JsonResponse({'details':details, 'panel':final_item},status =200)
        elif role == "Patient":
            patient_data = Patient.objects.filter(email = user).values()
            id = str(patient_data[0]['id'])
            item = Portal_items.objects.filter(user_type = role).values().order_by('order')
            details = []
            val = {
                'name':name,
                'speciality':"Patient ID:"+" "+id,
                'first_name':first_name
            }
            details.append(val)
            final_item=[]
            for info in item:
                value = {
                    'title':info['title'],
                    'icon':info['icon'],
                    'url':info['url']
                    }
                final_item.append(value)
            
            return JsonResponse({'details':details, 'panel':final_item},status =200)
        else:
            item = Portal_items.objects.filter(user_type = role).values().order_by('order')
            details=[]
            val = {
                'name':name,
                'speciality':role,
                'first_name':first_name
            }
            details.append(val)
            final_item=[]
            for info in item:
                value = {
                    'title':info['title'],
                    'icon':info['icon'],
                    'url':info['url']
                    }
                final_item.append(value)
            return JsonResponse({'details':details,'panel':final_item},status =200)
    else:
        return JsonResponse({'error':'Invalid method'},status =405)
        
        
def list_doctors(request):
    if request.method =="GET":
        doc = Doctor.objects.all().values()
        details =[]
        for det in doc:
            values = {
                'first_name':"Dr. " + det['first_name'],
                'last_name':det['last_name'],
                'specialist':det['specialist'],
                'experience':det['experience'],
                'consultation_fee':det['consultation_fee'],
                'qualification':det['qualification']
            }
            details.append(values)
        return JsonResponse({'details':details},status = 200)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)
    
def appointment_schedule(request):
    if request.method == "POST":
        email =request.user
        
        info = User.objects.filter(email = email).values()
        role = info[0]['role']
        id = info[0]['id']
        if role == "Patient":
            details = Patient.objects.filter(email = email).values()
        
            patientID = details[0]['id']
            first_name = details[0]['first_name']
            last_name = details[0]['last_name']
            
            phone_number = details[0]['phone_number']
            height = details[0]['height']
            weight = details[0]['weight']
            age = details[0]['age']
            blood_group = details[0]['blood_group']
            data= json.loads(request.body)
            preferred_date = data.get('preferred_date')
            symptoms = data.get('symptoms')
            speciality = data.get('speciality')
            doctor_selected = data.get('doctor_selected')
            reason = data.get('reason')
            
            Appointment.objects.create(user_id = id,email = email,patientID = patientID,name = first_name+" "+last_name,phone_number=phone_number,height = height,weight=weight,age=age,blood_group=blood_group,preferred_date=preferred_date,symptoms = symptoms,speciality =speciality,doctor_selected=doctor_selected,reason=reason)
            
        
            return JsonResponse({'message':'Appointment request sent.You will be updated via email,once it gets approved'},status =201)
        else:
            return JsonResponse({'error':'Only patients are allowed to schedule appointment'},status =400)
    else:
        return JsonResponse({'error':'Invalid method'},status = 405)
    
    
def list_specialisation(request):
    if request.method== "GET":
        details = Specialist.objects.all().values()
        doc_det =[]
        for item in details:
            value ={
                'id':item['id'],
                'name':item['specialist_name']
            }
            doc_det.append(value)
        return JsonResponse({'list':doc_det},status=200)
    else:
        return JsonResponse({'error':'Invalid method'},status =405)    
def spec_doc(request):
    if request.method =="POST":
        data = json.loads(request.body)
        specialisation = data.get('specialisation')
        doc = Doctor.objects.filter(specialist = specialisation).values()
        print(doc)
        details=[]
        for item in doc:
            value ={
                'name': "Dr."+" "+ item['first_name'] +" "+item['last_name']
            }
            details.append(value)
            
            
        return JsonResponse({'list':details},status = 200)
    else:
        return JsonResponse({'error':'Invalid Method'},status = 405)
    
def list_appointments(request):
    if request.method =="GET":
        email = request.user
        det = User.objects.filter(email = email).values()
        superuser = det[0]['is_superuser']
        if superuser== True:
            details = Appointment.objects.all().values()
            det=[]
            for item in details:
                value = {
                    'id':item['id'],
                    'name':item['name'],
                    'email':item['email'],
                    'doctor':item['doctor_selected'],
                    'preferred_date':item['preferred_date'],
                    'approved':item['is_approved_recep']   
                }
                det.append(value)
        
            return JsonResponse({'list':det},status  =200)
        else:
            return JsonResponse({'error':'Only Receptionist can access all appointments'},status =405)
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
        
    
def update_status(request):
    if request.method == "PATCH":
        email = request.user
        det = User.objects.filter(email = email).values()
        superuser = det[0]['is_superuser']
        if superuser== True:
            data = json.loads(request.body)
            id= data.get('id')
            remark = data.get('remark')
            is_approved = data.get('is_approved') 
            if not Appointment.objects.filter(id= id).exists():
                return JsonResponse({'error':'Please enter a valid appointment ID'},status = 405)
            details = Appointment.objects.filter(id =id).values()
            print(details)
            
            return JsonResponse({'msg':'Good'},status = 200)
        return JsonResponse({'error':'Only Receptionist can access all appointments'},status =405)
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)