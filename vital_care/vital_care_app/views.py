from django.templatetags.static import static
import re
from django_renderpdf.helpers import render_pdf

from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Doctor
from .models import Patient
from .models import Prescription
from .models import Specialist
from .models import Portal_items
from .models import Appointment



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
        
        
        date_of_birth = request.POST['date_of_birth']
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
        # mail =send_mail(
        #     " Account created",
        #     "Your VITALCURE patient account has been successfully created!!",
        #     "nandinisingh52891@gmail.com",
        #     [email],
        #     fail_silently=False
        # )
        # if not mail:
        #     return JsonResponse({"message":"Account created,but mail not sent!"},status =200)
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
        # mail = send_mail(
        #     " Account created",
        #     "Your VITALCURE doctor account has been successfully created!!",
        #     "nandinisingh52891@gmail.com",
        #     [email],
        #     fail_silently=False
        #     )
        # if not mail:
        #     return JsonResponse({"message":"Account created,but mail not sent!"},status =200)
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
        image = data[0]['image']
        role = data[0]['role']
        first_name = data[0]['first_name']
        last_name = data[0]['last_name']
        
        if role == "Doctor":
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
        elif role == "Patient":
            patient_data = Patient.objects.filter(email = user).values()
            id = str(patient_data[0]['id'])
            item = Portal_items.objects.filter(user_type = role).values().order_by('order')
            details = []
            name = first_name
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
        data = User.objects.filter(is_doctor=1).values()
        details =[]
        for det in doc:
            values = {
                'image':data[0]['image'],
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
        patient = Patient.objects.all().values()
        data = User.objects.filter(is_patient=1).values()
        details =[]
        for det in patient:
            val={
                'image':data[0]['image'],
                'first_name':det['first_name'],
                'last_name':det['last_name'],
                'email':det['email'],
                'phone_number':det['phone_number'],
                'height':det['height'],
                'weight':det['weight'],
                'age':det['age'],
                'gender':det['gender'],
                'blood_group':det['blood_group'],
                'medical_history':det['medical_history'],
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
        if role == "Patient":
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
            details = Appointment.objects.filter(visited = False).values()
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
            approved=1
            details.is_approved_doc = approved
            details.visited_doc = approved
            details.save()
            context = {
                'name':det[0]['name'],
            'doctor_selected':det[0]['doctor_selected'],
            'reason':det[0]['reason'],
            'preferred_date':det[0]['preferred_date']
            }
            print(context)
            pdf_file = render_pdf('confirm.html', context)
            email_subject = "Appointment Confirmation"
            email_body = "Please find attachment containing details of your appointment confirmation."
            email = EmailMessage(
            email_subject,
            email_body,
            'nandinisingh52891@gmail.com',
            [email_pat]
            )
    
            email.attach(f'appointment_{id}.pdf', pdf_file.content, 'application/pdf')
            email.send()
            return JsonResponse({"message":"Appointment approved"},status =200)
        
        
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
        #     send_mail(
        #     "Appointment rejected",
        #     "Your appointment request has been rejected due to the following reason: "+remark,
        #     "nandinisingh52891@gmail.com",
        #     [email_pat],
        #     fail_silently=False
        # )
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
            details.is_approved_recep = approved
            details.visited = visit
            details.visited_doc = visit
            details.save()
            info = Appointment.objects.filter(id=id).values()
            email_pat = info[0]['email']
        #     send_mail(
        #     "Appointment rejected",
        #     "Your appointment request has been rejected due to the following reason: "+remark,
        #     "nandinisingh52891@gmail.com",
        #     [email_pat],
        #     fail_silently=False
        # )
            
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
                    
                    'blood_group':item['blood_group'],
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
            num_pending = Appointment.objects.filter(visited =1).filter(is_approved_recep=1).filter(visited_doc=0).count()
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
            num_approved = Appointment.objects.filter(doctor_selected = name).filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).count()
            num_reject = Appointment.objects.filter(visited =1).filter(is_approved_recep=1).filter(visited_doc =1).filter(is_approved_doc=0).filter(doctor_selected = name).count()
            num_pending = Appointment.objects.filter(doctor_selected = name).filter(visited =1).filter(is_approved_recep=1).filter(visited_doc=0).count()
            details=[]
            val={
                'appointment_accepted':num_approved,
                'appointment_rejected':num_reject,
                'pending':num_pending,
                'role':role
            }
            details.append(val)
            
            return JsonResponse({'details':details},status =200)
        else:
            name = data[0]['first_name'] 
            app = Appointment.objects.filter(name =name).count()
            if app==0:
                return JsonResponse({'message':'No data found for this user'},status =200)
            num = Appointment.objects.filter(name = name).filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).count()
            app =Appointment.objects.filter(name = name).filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).filter(is_prescribed =1).values().order_by('-id')
            det=[]
            appp=Appointment.objects.filter(name = name).filter(visited =1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc =1).filter(is_prescribed =1).values()
            id = appp[0]['id']
            det = Prescription.objects.filter(appointment_id = id).values()
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
                'appointment_id':id,
                'instruction':item['instruction'],
                'diagnosis':item['diagnosis'],
                'medicine':date,  
                'role':role             
                }
            details.append(val)
            return JsonResponse({'list':details,'number':num},status =200)    
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
            det = Appointment.objects.filter(doctor_selected = name).filter(visited=1).filter(is_approved_recep =1).filter(visited_doc=1).filter(is_approved_doc=1).values()
        
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
            return JsonResponse({'details':info,'role':role},status = 200)
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
            data = Appointment.objects.filter(doctor_selected = name1).values().order_by('-id')
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
            data = Appointment.objects.filter(name = name).values().order_by('-id')
            details =[]
            for item in data:
                val = {
                    'id':item['id'],
                    'email':item['email'],
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
    else:
        return JsonResponse({'error':'Invalid Method'},status =405)
    
def create_prescription(request):
    if request.method == "POST":
        user = request.user
        user_det = User.objects.filter(email=user).values()
        role = user_det[0]['role']

        data = json.loads(request.body)
        appointment_id = data.get('appointment_id')
        instruction = data.get('instruction')
        diagnosis = data.get('diagnosis')
        day = data.get('day', [])
        print(day)
        dosage = data.get('dosage', [])
        print(dosage)
        medicines = data.get('medicine', [])
        print(medicines)
        print(len(day))
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
                diagnosis=diagnosis
            )
        Appointment.objects.filter(id=appointment_id).update(is_prescribed=1)

        return JsonResponse({'message': 'Prescription added'}, status=200)
    
    return JsonResponse({'error': 'Invalid method'}, status=405)
            
            
def list_prescription(request):
    if request.method =="GET":
        user = request.user
        user_det = User.objects.filter(email = user).values()
        role = user_det[0]['role']
        is_patient= user_det[0]['is_patient']
        if is_patient == True:
            name =user_det[0]['first_name']+ " "+ user_det[0]['last_name']
            app_det = Appointment.objects.filter(name = name).filter(is_prescribed = 1).values()
            id_list =[]
            for i in app_det:
                val={
                    i['id']
                }
                id_list.extend(val)
            print(id_list)
            
            for i in range(len(id_list)):
                print(i)
                ID = id_list[i]
                print(ID)
                details = Prescription.objects.filter(appointment_id =ID).values()
                det =[]
                date =[]        
                for item in details:
                    values = {
                    'medicine':item['medicine'],
                    'dosage':item['dosage'],
                    'days':item['days']
                    }
                    print(values)
                    date.append(values)
                    val = {
                    'appointment_id':ID,
                    'instruction':item['instruction'],
                    'diagnosis':item['diagnosis'],
                    'medicine':date                  
                    }
                    print(val)
                    det.insert(i,val)
                    print(det)
                    return JsonResponse({'list':det,'role':role},status =200)
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
        
    

            

            
            
        

        