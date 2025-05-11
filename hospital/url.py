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
    path('confirmregistration/<int:department_id>/<int:doctor_id>/<str:consultation_date>/<str:consultation_hours>/',
         ConfirmRegistrationView.as_view()),
    path('confirmregistration/', ConfirmRegistrationView.as_view()),
    path('patientshowregistration/', PatientShowRegistrationView.as_view()),
    path('healthtips/', HealthTipsView.as_view(), name='healthtips'),

    path('doctorcenter/', DoctorCenterView.as_view(), name='doctorcenter'),  # 添加 name 参数
    path('doctorshowregistration/', DoctorShowRegistrationView.as_view()),

    path('patientupdateinfo/', PatientUpdateInfoView.as_view(), name='patient_update_info'),
    path('evaluate_doctor/<int:register_id>/', EvaluateDoctorView.as_view(), name='evaluate_doctor'),
    path('patient_evaluation_records/', PatientEvaluationRecordsView.as_view(), name='patient_evaluation_records'),

    path('doctor_view_patient_evaluations/', DoctorViewPatientEvaluationsView.as_view()),
    path('doctorinfo/', DoctorInfoView.as_view(), name='doctorinfo'),

    path('patientcancelregistration/', PatientCancelRegistrationView.as_view(), name='patient_cancel_registration'),
    path('patientcancelregistration/<int:register_id>/', PatientCancelRegistrationView.as_view(), name='patient_cancel_registration_process'),

    path('ai_health_prediction/', AIHealthPredictionView.as_view(), name='ai_health_prediction'),
    path('random_diet_recommendation/', RandomDietRecommendationView.as_view(), name='random_diet_recommendation'),

    path('health_self_assessment/', HealthSelfAssessmentView.as_view(), name='health_self_assessment'),
    path('health_self_assessment_result/', HealthSelfAssessmentView.as_view(),name='health_self_assessment_result'),
]