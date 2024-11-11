import re
from django.template.loader import render_to_string
from weasyprint import HTML
from django_renderpdf.helpers import django_url_fetcher
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime
from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Doctor
from .models import Patient
from .models import Prescription
from .models import Specialist
from .models import Portal_items
from .models import Appointment
from .models import Blood_group



def patient_register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        if first_name is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                return JsonResponse({'error':'Please enter a valid first name'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid first name'},status =400)
        
        last_name = request.POST['last_name']
        
        
        
        email = request.POST['email']
        if email is not None:
            if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                return JsonResponse({'error':'Please enter a valid email'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid email ID'},status =400)
        
        phone_number =request.POST['phone_number']
        if phone_number is not None:
            if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        if len(request.FILES)!= 0:
            image = request.FILES['image']
        else:
            return JsonResponse({'error':'Please upload a valid image '},status =400)
        
        height = str(request.POST['height'])
        if height is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",height)):
                return JsonResponse({'error':'Please enter valid height'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid height'},status =400)
        
        weight = str(request.POST['weight'])
        if weight is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",weight)):
                return JsonResponse({'error':'Please enter  weight'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid weight'},status =400)
        
        age = str(request.POST['age'])
        if age is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",age)):
                return JsonResponse({'error':'Please enter valid age'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid age'},status =400)
        
        gender = request.POST['gender']
        if gender is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",gender)):
                return JsonResponse({'error':'Please enter valid gender'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid gender'},status =400)
        
        
        blood_group = request.POST['blood_group']
        if blood_group is not None:
            if not bool(re.match(r"^(A|B|AB|O)[+-]$",blood_group)):
                return JsonResponse({'error':'Please enter valid blood group'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid blood group'},status =400)
        
        medical_history =request.POST['medical_history']
        
        
        
        date_of_birth= request.POST['date_of_birth']
        
        if date_of_birth is  None:
            return JsonResponse({'error':'Please enter valid date of birth'},status =400)

        
        address = request.POST['address']
        if address is None:
            return JsonResponse({'error':'Please enter a valid address '} ,status =400)
        password = request.POST['password']
        cpassword =  request.POST['cpassword']
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
            return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):
            return JsonResponse({'error':'password must  contain at least a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'error': 'User already exists!!,please try with another email address'},status=400)
        

        user = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,role = "Patient",is_doctor=0,is_patient=1,password=password,image = image)
        Patient.objects.create(user =user,email =email,first_name = first_name,last_name = last_name,phone_number= phone_number,height = height,weight =weight,age =age,gender = gender,blood_group = blood_group,medical_history = medical_history,date_of_birth=date_of_birth,address=address)
        mail =send_mail(
            " Account created",
            "Your VITALCURE patient account has been successfully created!!",
            "nandinisingh52891@gmail.com",
            [email],
            fail_silently=False
        )
        if not mail:
            return JsonResponse({"message":"Account created,but mail not sent!"},status =200)
        return JsonResponse({'message':'Patient Account created successfully!!'},status = 201)

    else:
        return JsonResponse({'error':'Invalid method'},status =405)
    
    
def doctor_register(request):
    if request.method=="POST":
        first_name = request.POST['first_name']
        if first_name is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,29}$",first_name)):
                return JsonResponse({'error':'Please enter a valid first name'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid first name'},status =400)
        
        last_name = request.POST['last_name']
        
        
        email = request.POST['email']
        if email is not None:
            if not bool(re.match(r"[A-Za-z0-9\._%+\-]+@[A-Za-z0-9\.\-]+\.[A-Za-z]{2,}",email)):
                return JsonResponse({'error':'Please enter a valid email'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid email ID'},status =400)
        
        if len(request.FILES)!= 0:
            image = request.FILES['image']
        else:
            return JsonResponse({'error':'Please upload a valid image '},status =400)
        
        age = str(request.POST['age'])
        if age is not None:
            if not bool(re.match(r"^[0-9]\d*(\.\d+)?$",age)):
                return JsonResponse({'error':'Please enter valid age'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid age'},status =400)
        
        phone_number = request.POST['phone_number']
        if phone_number is not None:
            if not bool(re.match(r"^[6-9]{1}[0-9]{9}$",phone_number)):
                return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid phone number'},status =400)
        gender = request.POST['gender']
        if gender is not None:
            if not bool(re.match(r"^[A-Za-z]{1}[A-Z a-z]{1,15}$",gender)):
                return JsonResponse({'error':'Please enter valid gender'},status =400)
        else:
            return JsonResponse({'error':'Please enter valid gender'},status =400)
        specialist = request.POST['specialist']
        if specialist is None:
            return JsonResponse({'error':'Please a enter valid speciality'},status =400)
        qualification = request.POST['qualification']
        if qualification is None:
            return JsonResponse({'error':'Please a enter valid qualification'},status =400)
        consultation_fee = str(request.POST['consultation_fee'])
        if consultation_fee is not None:
            if not bool(re.match(r"^[0-9]*$",consultation_fee)):
                return JsonResponse({'error':'Please enter a valid consultation fee'},status =400)
        else:
            return JsonResponse({'error':'Please enter a valid consultation fee'},status =400)
        experience=request.POST['experience']
        password = request.POST['password']
        cpassword =  request.POST['cpassword']
        speacialist_id = Specialist.objects.filter(specialist_name =specialist).values()
        spec_id = speacialist_id[0]['id']
        

        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",password)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if not bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,16}$",cpassword)):
            return JsonResponse({'error':'password must  contain atleast a special character,a uppercase letter, a lowercase letter,a number and minimum should be of 8 character'},status =400)
        if password != cpassword:
            return JsonResponse({'error':'Password and confirm password do not match'},status = 400)
        
        
        if User.objects.filter(email = email).exists():
            return JsonResponse({'error': 'User already exists!!,please try with another email address'},status=400)
        user  = User.objects.create_user(email=email,first_name=first_name,last_name=last_name,role = "Doctor",is_doctor=1,is_patient=0,password=password ,image =image)
        Doctor.objects.create(user = user ,spec_id = spec_id,email =email,first_name = first_name,last_name = last_name,phone_number= phone_number,age=age,gender = gender,specialist=specialist,experience =experience,qualification=qualification,consultation_fee = consultation_fee)
        mail = send_mail(
            " Account created",
            "Your VITALCURE doctor account has been successfully created!!",
            "nandinisingh52891@gmail.com",
            [email],
            fail_silently=False
            )
        if not mail:
            return JsonResponse({"message":"Account created,but mail not sent!"},status =200)
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
            if role =="R":
                return JsonResponse({'message':'Receptionist successfully logged in!'},status =200)
            elif role=="D":
                return JsonResponse({'message':'Doctor successfully logged in!'},status =200)
            elif role=="P":
                return JsonResponse({'message':'Patient successfully logged in!'},status =200)

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
        image = data[0]['image']
        role = data[0]['role']
        first_name = data[0]['first_name']
        last_name = data[0]['last_name']
        
        if role == "D":
            doc_data = Doctor.objects.filter(email = user).values()
            speciality = doc_data[0]['specialist']
            details =[]
            name = first_name+ " " + last_name
            val = {
                'image':image,
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
        elif role == "P":
            patient_data = Patient.objects.filter(email = user).values()
            id = str(patient_data[0]['id'])
            item = Portal_items.objects.filter(user_type = role).values().order_by('order')
            details = []
            name = first_name+" "+last_name
            val = {
                'image':image,
                'name':name,
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
            name = first_name+ " " + last_name
            
            
            val = {
                'image':image,
                'name':name,
                'speciality':"Receptionist",
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
        data = User.objects.filter(is_doctor=1).values()
        id_list=[]
        for i in range(len(data)):
            id = data[i]['id']
            id_list.append(id)
        details =[]
        for id in id_list:
            doc_data = User.objects.filter(id =id).values()
            doc_details = Doctor.objects.filter(user_id =id).values()
            img = doc_data[0]['image']
            for det in doc_details :
                values = {
                    
                    'img':img,
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

def list_patients(request):
    if request.method=="GET":
        data = User.objects.filter(is_patient=1).values()
        id_list=[]
        details=[]
        for i in range(len(data)):
            id = data[i]['id']
            id_list.append(id)
        for id in id_list:
            pat_data = User.objects.filter(id =id).values()
            pat_details = Patient.objects.filter(user_id =id).values()
            img = pat_data[0]['image']
            
            for det in pat_details:

                val={
                'image':img,
                'first_name':det['first_name'],
                'last_name':det['last_name'],
                'email':det['email'],
                'phone_number':det['phone_number'],
                'height':det['height'],
                'weight':det['weight'],
                'age':det['age'],
                'gender':det['gender'],
                'blood_group':det['blood_group'],
                'medical_history':det['medical_history']or "NULL",
                'date_of_birth':det['date_of_birth'],
                'address':det['address']
                }
                details.append(val)
        return JsonResponse({'details':details},status =200)
    else:
        return JsonResponse({'error':'Invalid method'},status =405)
    
def appointment_schedule(request):
    if request.method == "POST":
        user = request.user
        data = User.objects.filter(email=user).values()
        role = data[0]['role']
        role =data[0]['role']
        id = data[0]['id']
        if role == "P":
            details = Patient.objects.filter(email = user).values()
        
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
            
            Appointment.objects.create(user_id = id,email = user,patientID = patientID,name = first_name+" "+last_name,phone_number=phone_number,height = height,weight=weight,age=age,blood_group=blood_group,preferred_date=preferred_date,symptoms = symptoms,speciality =speciality,doctor_selected=doctor_selected,reason=reason)
            
        
            return JsonResponse({'message':'Appointment request sent. You will be updated via email, once it gets approved.'},status =201)
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
    
def list_blood_group(request):
    if request.method=="GET":
        det = Blood_group.objects.all().values()
        details =[]
        for item in det:
            val = {
                'id':item['id'],
            'blood_grp':item['blood_group']
            }
            details.append(val)
        return JsonResponse({'list':details},status = 200)
    else:
        return JsonResponse({'error':'Invalid Method'},status=405)
def spec_doc(request):
    if request.method =="POST":
        data = json.loads(request.body)
        specialisation = data.get('specialisation')
        doc = Doctor.objects.filter(specialist = specialisation).values()
        details=[]
        for item in doc:
            value ={
                'name': "Dr."+" "+ item['first_name'] +" "+item['last_name'],
                'fee':item['consultation_fee']
            }
            details.append(value)
            
            
        return JsonResponse({'list':details},status = 200)
    else:
        return JsonResponse({'error':'Invalid Method'},status = 405)
    
def list_appointments(request):
    if request.method =="GET":
        email = request.user
        det = User.objects.filter(email = email).values()
        role = det[0]['role']
        superuser = det[0]['is_superuser']
        is_doctor = det[0]['is_doctor']
        if superuser== True:
            details = Appointment.objects.filter(is_deleted = False).filter(visited = False).values()
            det=[]
            for item in details:

                value = {
                    'id':item['id'],
                    'name':item['name'],
                    'email':item['email'],
                    'doctor':item['doctor_selected'],
                    'preferred_date':item['preferred_date'],
                    'reason':item['reason']
                }
                det.append(value)
        
            return JsonResponse({'list':det,'role':role},status  =200)
        elif is_doctor == True:
            first_name = det[0]['first_name']
            last_name = det[0]['last_name']
            name = "Dr. "+first_name+" "+last_name
            details = Appointment.objects.filter(is_approved_recep = True).values()
            doc_det = details.filter(doctor_selected = name).values()
            details_final = doc_det.filter(visited_doc = 0).values()

            det =[]
            for item in details_final:

                values={
                    'id':item['id'],
                    'name':item['name'],
                    'email':item['email'],
                    'preferred_date':item['preferred_date'],
                    'reason':item['reason']
                }
                det.append(values)
            
            return JsonResponse({'list':det,'role':role},status =200)
        
        else:
            return JsonResponse({'msg':'Invalid User'},status =400)
            
        
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)


def approve_appoint(request):
    if request.method == "PATCH":
        email = request.user
        det = User.objects.filter(email = email).values()
        superuser = det[0]['is_superuser']
        is_doctor = det[0]['is_doctor']

        if superuser== True:
            data = json.loads(request.body)
            id= data.get('id')
            if not Appointment.objects.filter(id= id).exists():
                return JsonResponse({'error':'Please enter a valid appointment ID'},status = 400)
            details = Appointment.objects.get(id =id)
            approved=1
            visit =1
            details.is_approved_recep = approved
            details.visited = visit
            details.save()
            return JsonResponse({'message':'Appointment approved'},status = 200)
        
        elif is_doctor==True:
            data = json.loads(request.body)
            id= data.get('id')
            if not Appointment.objects.filter(id= id).exists():
                return JsonResponse({'error':'Please enter a valid appointment ID'},status = 400)
            details = Appointment.objects.get(id =id)
            det = Appointment.objects.filter(id=id).values()
            email_pat = det[0]['email']
            date= det[0]['preferred_date']
            f_date = format_date(date)
            print(f_date)
            approved=1
            details.is_approved_doc = approved
            details.visited_doc = approved
            details.save()
            context = {
            'name':det[0]['name'],
            'doctor_selected':det[0]['doctor_selected'],
            'reason':det[0]['reason'],
            'preferred_date':f_date
            }
            print(context)
            
            pdf_file= BytesIO()
            url_fetcher=django_url_fetcher
            template = 'confirm.html'
            
            html_content = render_to_string('confirm.html', context)
            
            pdf = HTML(string=html_content).write_pdf()
            pdf_file = BytesIO(pdf)
            
            pdf_size = pdf_file.getbuffer().nbytes
            if pdf_size == 0:
                return JsonResponse({'message': 'Appointment approved but PDF generation failed!'}, status=200)

            email_subject = "Appointment Confirmation"
            email_body = "Please find attached the details of your appointment confirmation."
            email = EmailMultiAlternatives(
                email_subject,
                email_body,
                'nandinisingh52891@gmail.com',  
                [email_pat] 
            )
            

            pdf_content = pdf_file.read()
            email.attach(f'appointment_{id}.pdf', pdf_content, 'application/pdf')
            email.send()
            return JsonResponse({"message": "Appointment approved"}, status=200)
        
        
        else:
            return JsonResponse({'message':'Invalid User'},status =400)
        
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
    

    
def reject_appoint(request):
    if request.method == "PATCH":
        email = request.user
        det = User.objects.filter(email = email).values()
        superuser = det[0]['is_superuser']
        is_doctor = det[0]['is_doctor']

        if superuser== True:
            data = json.loads(request.body)
            id= data.get('id')
            remark = data.get('remark')
            if not Appointment.objects.filter(id= id).exists():
                return JsonResponse({'error':'Please enter a valid appointment ID'},status = 400)
            details = Appointment.objects.get(id =id)
            approved=0
            visit =1
            details.remark = remark
            details.is_approved_recep = approved
            details.visited = visit
            details.save()
            info = Appointment.objects.filter(id=id).values()
            email_pat = info[0]['email']
            send_mail(
            "Appointment rejected",
            "Your appointment request has been rejected due to the following reason: "+remark,
            "nandinisingh52891@gmail.com",
            [email_pat],
            fail_silently=False
        )
            return JsonResponse({'message':'Appointment rejected'},status = 200)
    
        
        elif is_doctor==True:
            data = json.loads(request.body)
            id= data.get('id')
            remark = data.get('remark')
            if not Appointment.objects.filter(id= id).exists():
                return JsonResponse({'error':'Please enter a valid appointment ID'},status = 400)
            details = Appointment.objects.get(id =id)
            approved=0
            visit =1
            details.remark = remark
            details.visited_doc = visit
            details.is_approved_doc=approved
            details.save()
            info = Appointment.objects.filter(id=id).values()
            email_pat = info[0]['email']
            send_mail(
            "Appointment rejected",
            "Your appointment request has been rejected due to the following reason: "+remark,
            "nandinisingh52891@gmail.com",
            [email_pat],
            fail_silently=False
        )
            
            return JsonResponse({'message':'Appointment rejected'},status = 200)
        
        else:
            return JsonResponse({'message':'Invalid User'},status = 400)
            
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
    
    
def profile_details(request):
    if request.method=="GET":
        user = request.user
        
        data = User.objects.filter(email=user).values()
        role = data[0]['role']
        is_superuser = data[0]['is_superuser']
        is_doctor = data[0]['is_doctor']
        is_patient = data[0]['is_patient']
        if is_superuser == True:
            f_name = data[0]['first_name']
            l_name = data[0]['last_name']
            name = f_name + " "+ l_name
            details = []
            for item in data:
                value ={
                    'name':name,
                    'email':item['email'],
                    'role':item['role']
                }
                details.append(value)
            return JsonResponse({'profile':details},status = 200)
        elif is_doctor ==True:
            data = Doctor.objects.filter(email = user).values()
            f_name = data[0]['first_name']
            l_name = data[0]['last_name']
            name = f_name + " "+ l_name
            details = []
            for item in data:
                val = {
                    'id':item['id'],
                    'name':name,
                    'email':item['email'],
                    'phone_number':item['phone_number'],
                    'specialist':item['specialist'],
                    'experience':item['experience'],
                    'age':item['age'],
                    'qualification':item['qualification'],
                    'consultation_fee':item['consultation_fee'],
                    'role':role,

                }
                details.append(val)
            return JsonResponse({'profile':details},status =200)
        
        elif is_patient == True:
            data = Patient.objects.filter(email = user).values()
            f_name = data[0]['first_name']
            l_name = data[0]['last_name']
            name = f_name + " "+ l_name
            details = []
            for item in data:

                val = {
                    'id':item['id'],
                    'name':name,
                    'email':item['email'],
                    'phone_number':item['phone_number'],
                    'height':item['height'],
                    'weight':item['weight'],
                    'age':item['age'],
                    'date_of_birth':item['date_of_birth'],
                    'medical_history':item['medical_history'],
                    'blood_group':item['blood_group'],
                    'address':item['address'],
                    'role':role
                    }
                details.append(val)
            return JsonResponse({'profile':details},status = 200)
        else:
            return JsonResponse({'error':'Invalid user'},status = 400)
    else:
        return JsonResponse({'error':'Invalid Method'},status = 405)
    
    
def stats(request):
    if request.method =="GET":
        user= request.user
        data = User.objects.filter(email=user).values()
        users_id = data[0]['id']
        
        role = data[0]['role']
        is_superuser = data[0]['is_superuser']
        is_doctor = data[0]['is_doctor']
        pat =data[0]['is_patient']
        
        if is_superuser ==True:
            num_docregister = Doctor.objects.all().count()
        
            num_pat_register = Patient.objects.all().count()
            
            num_appoint = Appointment.objects.all().count()
            num_app = Appointment.objects.filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).count()
            num_reject_recep = Appointment.objects.filter(visited=1).filter(is_approved_recep =0).count()
            num_reject_doc = Appointment.objects.filter(visited =1).filter(is_approved_recep=1).filter(visited_doc =1).filter(is_approved_doc =0).count()
            num_reject = num_reject_recep + num_reject_doc
            num_pending_recep = Appointment.objects.filter(visited=0).count()
            num_pending_doc = Appointment.objects.filter(visited =1).filter(is_approved_recep=1).filter(visited_doc=0).count()
            num_pending =num_pending_doc+num_pending_recep
            details =[]
            val ={
                'doctor_registered':num_docregister,
                'patient_registered':num_pat_register,
                'total_appointment':num_appoint,
                'appointment_accepted':num_app,
                'appointment_rejected':num_reject,
                'pending':num_pending,
                'role' : role
                
            }
            details.append(val)
            
            
            return JsonResponse({'details':details},status=200)
        elif is_doctor==True:
            name = "Dr."+" " +data[0]['first_name'] + " "+ data[0]['last_name']
            num = Appointment.objects.filter(doctor_selected = name).filter(visited =1).filter(is_approved_recep =1).count()
            num_approved = Appointment.objects.filter(doctor_selected = name).filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).count()
            num_reject = Appointment.objects.filter(visited =1).filter(is_approved_recep=1).filter(visited_doc =1).filter(is_approved_doc=0).filter(doctor_selected = name).count()
            num_pending = Appointment.objects.filter(doctor_selected = name).filter(visited =1).filter(is_approved_recep=1).filter(visited_doc=0).count()
            details=[]
            val={
                'total_appointment':num,
                'appointment_accepted':num_approved,
                'appointment_rejected':num_reject,
                'pending':num_pending,
                'role':role
            }
            details.append(val)
            
            return JsonResponse({'details':details},status =200)
        else:
            name = data[0]['first_name']+" " + data[0]['last_name']
            app = Appointment.objects.filter(name =name).count()
            if app==0:
                return JsonResponse({'message':'No data found for this user'},status =200)
            app =Appointment.objects.filter(name = name).values().order_by('-id').first()
            
            if app['visited']==1 and app['is_approved_recep'] ==1 and app['visited_doc']==1 and app['is_approved_doc']==1:
                status = "Approved"
            elif (app['visited']==1 and app['is_approved_recep'] ==0) or (app['visited_doc']==1 and app['is_approved_doc']==0):
                status = "Rejected"
            else:
                status = "Pending"
            rec_app = {
                    'reason':app['reason'],
                    'preferred_date':app['preferred_date'],
                    'doctor':app['doctor_selected'],
                    'status':status
                    }
            recent_pres = Prescription.objects.filter(user_id =users_id).values().order_by('-id').first()
            app_id = recent_pres['appointment_id']
            det = Prescription.objects.filter(appointment_id = app_id).values()       
            date_info = Appointment.objects.filter(id = app_id).values()
            app_date = date_info[0]['preferred_date']
            details =[]
            date =[]
            
            for item in det:
                values = {
                    'medicine':item['medicine'],
                    'dosage':item['dosage'],
                    'days':item['days']
                }
                date.append(values)
            val = {
                'date':app_date,
                'instruction':item['instruction'],
                'diagnosis':item['diagnosis'],
                'medicine':date, 
                'role':role             
                }
            details.append(val)
            list1 = []
            list1.append(rec_app)
            list1.append(details)
            return JsonResponse({'details':list1},status =200)    
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)           
    
def doc_patients(request):
    if request.method == "GET":
        user  =request.user
        user_det = User.objects.filter(email = user).values()
        is_doctor = user_det[0]['is_doctor']
        role = user_det[0]['role']
        if is_doctor ==True:
            doc_det = Doctor.objects.filter(email =user).values()
            name = "Dr. "+doc_det[0]['first_name']+ " "+ doc_det[0]['last_name']
            det = Appointment.objects.filter(doctor_selected = name).filter(visited=1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc=1).values().order_by('is_prescribed')
        
            info =[]
            for item in det:

                val = {
                    'id':item['id'],
                'name':item['name'],
                'email':item['email'],
                'date_of_appointment':item['preferred_date'],
                'reason':item['reason'],
                'symptoms':item['symptoms'] or "NULL",
                'is_prescribed':item['is_prescribed']
                }
                info.append(val)
            return JsonResponse({'details':info},status = 200)
        else:
            return JsonResponse({'error':'You are not allowed to access this page'},status =400)
    else:
        return JsonResponse({'error':'Invalid Method'},status = 405)
    
def list_appointment_reports(request):
    if request.method == "GET":
        user =request.user
        user_det = User.objects.filter(email = user).values()
        is_superuser = user_det[0]['is_superuser']
        role = user_det[0]['role']
        is_doctor = user_det[0]['is_doctor']
        is_patient= user_det[0]['is_patient']
        if is_superuser==True:
            data = Appointment.objects.all().values().order_by('-id')
            details =[]
            for item in data:

                val = {
                    'id':item['id'],
                    'email':item['email'],
                    'name':item['name'],
                    'phone_number':item['phone_number'],
                    'preferred_date':item['preferred_date'],
                    'doctor':item['doctor_selected'],
                    'reason':item['reason']
                }
                details.append(val)
                if item['is_approved_doc'] == 1:
                    status = "Approved"
                    val["status"] = status
                elif item['visited_doc'] == 1 and item['is_approved_doc']==0:
                    status = "Rejected"
                    val["status"] = status

                else:
                    status = "Pending"
                    val["status"] = status 
            return JsonResponse({'details':details,'url':'records','role':role},status =200)
        elif is_doctor == True:
            name1 = "Dr. "+ user_det[0]['first_name']+ " " + user_det[0]['last_name']
            data = Appointment.objects.filter(doctor_selected = name1).filter(visited =1).filter(is_approved_recep=1).values().order_by('-id')
            details =[]
            for item in data:

                val = {
                    'id':item['id'],
                    'email':item['email'],
                    'preferred_date':item['preferred_date'],
                    'name':item['name'],
                    'reason':item['reason']
                }
                details.append(val)
                if item['is_approved_doc'] == 1:
                    status = "Approved"
                    val["status"] = status
                elif item['visited_doc'] == 1 and item['is_approved_doc']==0:
                    status = "Rejected"
                    val["status"] = status

                else:
                    status = "Pending"
                    val["status"] = status 
            return JsonResponse({'details':details,'url':'records','role':role},status =200)
        else:
            name = user_det[0]['first_name']+ " "+ user_det[0]['last_name']
            data = Appointment.objects.filter(name = name).filter(is_deleted =False).values().order_by('-id')
            details =[]
            for item in data:
                
                val = {
                    'id':item['id'],
                    'email':item['email'],
                    'preferred_date':item['preferred_date'],
                    'doctor':item['doctor_selected'],
                    'reason':item['reason'],
                    'visited_recep':item['visited']
                }
                details.append(val)
                if item['is_approved_doc'] == 1:
                    status = "Approved"
                    val["status"] = status
                elif (item['visited_doc'] == 1 and item['is_approved_doc']==0) or (item['visited']==1 and item['is_approved_recep']==0):
                    status = "Rejected"
                    val["status"] = status

                else:
                    status = "Pending"
                    val["status"] = status 
            return JsonResponse({'details':details,'url':'records','role':role},status =200)
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
    
def create_prescription(request):
    if request.method == "POST":
        user = request.user
        user_det = User.objects.filter(email=user).values()
        role = user_det[0]['role']
        doctor = "Dr. "+user_det[0]['first_name']+" "+user_det[0]['last_name']
        

        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        instruction = data.get('instruction')
        diagnosis = data.get('diagnosis')
        day = data.get('day', [])
        dosage = data.get('dosage', [])
        medicines = data.get('medicine', [])
        app_det = Appointment.objects.filter(id =appointment_id).values()
        users_id = app_det[0]['user_id']
        for i in range(len(day)):
        
            days = day[i] 
            dose = dosage[i]
            medicine_name = medicines[i]
            pres = Prescription.objects.create(
                appointment_id=appointment_id,
                instruction=instruction,
                medicine=medicine_name,
                dosage=dose,
                days=days,
                diagnosis=diagnosis,
                user_id =users_id
            )
        Appointment.objects.filter(id=appointment_id).update(is_prescribed=1)
        app_det = Appointment.objects.filter(id= appointment_id).values()
        email_pat = app_det[0]['email']
        
        det = Prescription.objects.filter(appointment_id = appointment_id).values()
        instruction = det[0]['instruction']
        diagnosis = det[0]['diagnosis']
        zipped_prescriptions = zip(medicines, dosage, day)
        
        final_dict = {
            'doctor': doctor,
            'diagnosis': diagnosis,
            'instruction': instruction,
            'prescriptions': list(zipped_prescriptions),
        }
        pdf_file= BytesIO()    
        html_content = render_to_string('prescription.html',final_dict)
            
        pdf = HTML(string=html_content).write_pdf()
        pdf_file = BytesIO(pdf)
        
        pdf_size = pdf_file.getbuffer().nbytes
        if pdf_size == 0:
            return JsonResponse({'message': 'Prescription added but PDF generation failed!'}, status=200)

        email_subject = "Prescription added!"
        email_body = "Please find the detailed prescription in attachment."
        email = EmailMultiAlternatives(
            email_subject,
            email_body,
            'nandinisingh52891@gmail.com',  
            [email_pat] 
        )
        pdf_content = pdf_file.read()
        email.attach(f'appointment_{appointment_id}.pdf', pdf_content, 'application/pdf')
        email.send()
        return JsonResponse({'message': 'Prescription added'}, status=200)
    return JsonResponse({'error': 'Invalid method'}, status=405)
            
            
def list_prescription(request):
    if request.method =="GET":
        user = request.user
        user_det = User.objects.filter(email = user).values()
        is_patient= user_det[0]['is_patient']
        if is_patient == True:
            name =user_det[0]['first_name']+ " "+ user_det[0]['last_name']
            det = Appointment.objects.filter(name = name).filter(is_prescribed = 1).count()
            if det==0:
                return JsonResponse({'message':'Currently, no data exists for this user'},status =200)
            app_det = Appointment.objects.filter(name = name).filter(is_prescribed = 1).values()
            
            list2=[]
            for item in app_det:
                date = item['preferred_date']
                doctor = item['doctor_selected']
                id = item['id']
                pres_det = Prescription.objects.filter(appointment_id = id).values()
                cnt_pres = Prescription.objects.filter(appointment_id = id).count()
                list1=[]
                if cnt_pres==0:
                    return JsonResponse({'message':'Currently, no data exists for this user'},status =200)
                for item in pres_det:
                    values = {
                    'medicine':item['medicine'],
                    'dosage':item['dosage'],
                    'days':item['days']
                    }
                    list1.append(values)
                val = {
                        'id':id,
                        'date':date,
                        'doctor':doctor,
                        'instruction':item['instruction'],
                        'diagnosis':item['diagnosis'],
                        'medicine':list1, 
                    }
                list2.append(val)                
            return JsonResponse({'list':list2},status =200)
        else:
            return JsonResponse({'error':'You are not allowed to access this page!'},status = 400)
    else:
        return JsonResponse({'error':'Invalid method'},status =405)
    
def list_doc_pres(request):
    if request.method=="POST":
        user = request.user
        user_det = User.objects.filter(email = user).values()
        role = user_det[0]['role']
        doc = user_det[0]['is_doctor']
        if doc==True:

            data = json.loads(request.body)
            app_id = data.get('appointment_id')
            if not Prescription.objects.filter(appointment_id = app_id).exists():
                return JsonResponse({'error':'Prescription of this appointment is not given!!'},status =400)
            details = Prescription.objects.filter(appointment_id = app_id).values()
            det =[]
            date =[]
            
            for item in details:
                values = {
                    'medicine':item['medicine'],
                    'dosage':item['dosage'],
                    'days':item['days']
                }
                date.append(values)
            val = {
                'appointment_id':app_id,
                'instruction':item['instruction'],
                'diagnosis':item['diagnosis'],
                'medicine':date                  
                }
            det.append(val)
            return JsonResponse({'list':det,'role':role},status =200)
        else:
            return JsonResponse({'error':'You are not allowed to access this page!'},status = 400)
    else:
        return JsonResponse({'error':'Invalid method'},status =405)

def delete_appointment(request):
    if request.method =="PATCH":
        user = request.user
        user_det = User.objects.filter(email = user).values()
        pat = user_det[0]['is_patient']
        if pat:
            data = json.loads(request.body)
            id = data.get('id')
            if Appointment.objects.filter(id = id).exists():
                Appointment.objects.filter(id = id).update(is_deleted =1)
                return JsonResponse({'message':'Appointment successfully deleted'},status = 200)
            else:
                return JsonResponse({'error':'Appointment ID is invalid'},status =400)
        else:
            return JsonResponse({'error':'You are not allowed to delete appointment'},status =401)
            
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
        
        
def format_date(date_string):
    date_obj = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")
    f_date = date_obj.strftime("%Y-%m-%d")
    return f_date
            

            
            
        

        