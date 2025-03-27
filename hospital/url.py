# HospitalSystem/hospital/url.py
from django.urls import path
from .views import *

# 挂号预约子路由
urlpatterns = [
    path('', ChooseLoginView.as_view()),
    path('patientlogin/', PatientLoginView.as_view()),
    path('doctorlogin/', DoctorLoginView.as_view()),
    path('patientregister/', PatientRegisterView.as_view()),

    path('patientcenter/', PatientCenterView.as_view(), name='patientcenter'),  # 添加 name 参数
    path('choosedepartment/', ChooseDepartmentView.as_view()),
    path('choosedoctorandtime/<int:department_id>/', ChooseDoctorAndTimeView.as_view()),
    path('confirmregistration/<int:department_id>/<int:doctor_id>/<str:consultation_hours>/',
         ConfirmRegistrationView.as_view()),
    path('confirmregistration/', ConfirmRegistrationView.as_view()),
    path('patientshowregistration/', PatientShowRegistrationView.as_view()),
    path('traffic/', TrafficView.as_view()),

    path('doctorcenter/', DoctorCenterView.as_view()),
    path('doctorshowregistration/', DoctorShowRegistrationView.as_view()),

    path('patientupdateinfo/', PatientUpdateInfoView.as_view(), name='patient_update_info'),
    path('evaluate_doctor/<int:register_id>/', EvaluateDoctorView.as_view(), name='evaluate_doctor'),
    path('patient_evaluation_records/', PatientEvaluationRecordsView.as_view(), name='patient_evaluation_records'),
]
