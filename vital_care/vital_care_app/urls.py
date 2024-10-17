from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('patient_register/',views.patient_register),
    path('doctor_register/',views.doctor_register),
    path('login_user/',views.login_user),
    path('logout_user/',views.logout_user),
    path('view_panel/',views.side_menu),
    path('list_doctors/',views.list_doctors),
    path('appointment_schedule/',views.appointment_schedule),
    path('list_specialisation/',views.list_specialisation),
    path('spec_doctor/',views.spec_doc),
    path('list_appoint/',views.list_appointments),
    path('approve_status/',views.approve_appoint),
    path('reject_appoint/',views.reject_appoint),
    path('profile_details/',views.profile_details),
    path('stats/',views.stats),
    path('doc_pat/',views.doc_patients),
    path('records/',views.list_appointment_reports),
    path('create_pres/',views.create_prescription),
    path('list_pres/',views.list_prescription),
    path('list_doc_pres/',views.list_doc_pres),
    path('list_patients/',views.list_patients),
    
    
    
    
    
    
    
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
