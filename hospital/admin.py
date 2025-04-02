from django.contrib import admin
from .models import *
from django import forms
from django.core.exceptions import ValidationError

admin.site.site_header = '医伴无忧 - 医院挂号预约平台后台管理系统'
admin.site.index_title = '首页'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address')
    search_fields = ['name', 'address']
    list_filter = ('name', 'address')
    ordering = ['id']


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sex', 'age', 'phone', 'password')
    search_fields = ['id', 'name', 'sex', 'age', 'phone', 'password']
    list_filter = ('id', 'name', 'sex', 'age', 'phone', 'password')
    ordering = ['id']


class DoctorAdminForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            qs = Doctor.objects.filter(phone=phone)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("该手机号码已被注册，请使用其他号码。")
        return phone

class DoctorAdmin(admin.ModelAdmin):
    form = DoctorAdminForm
    list_display = (
        'id', 'name', 'sex', 'age', 'department', 'level', 'registration_price', 'description', 'phone', 'password')
    search_fields = ['id', 'name', 'sex', 'age', 'department', 'level', 'registration_price', 'description', 'phone',
                     'password']
    list_filter = ('id', 'name', 'registration_price', 'age', 'level', 'department')
    ordering = ['id']


class TimeNumberAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'doctor', 'eight', 'nine', 'ten', 'eleven', 'fourteen', 'fifteen', 'sixteen', 'seventeen',
        'default_number')
    search_fields = ['id', 'doctor__name']
    list_filter = ('id', 'doctor__name')
    ordering = ['id']


class RegisterAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'patient', 'doctor', 'registration_time', 'consultation_hours', 'illness', 'address',
        'out_trade_num', 'status', 'payway',
    )
    search_fields = ['id', 'patient', 'doctor', 'registration_time', 'consultation_hours', 'illness',
                     'address', 'isdelete', 'out_trade_num', 'status', 'payway',
                     ]
    list_filter = (
        'id', 'patient', 'doctor', 'registration_time', 'consultation_hours', 'illness', 'address',
        'out_trade_num', 'status', 'payway',
    )
    ordering = ['id']


class DoctorEvaluationAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient', 'doctor', 'service_attitude', 'professional_level', 'comment', 'evaluation_time')
    search_fields = ['patient__name', 'doctor__name']
    list_filter = ('doctor__name', 'service_attitude', 'professional_level')
    ordering = ['-evaluation_time']


admin.site.register(Patient, PatientAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(TimeNumber, TimeNumberAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(DoctorEvaluation, DoctorEvaluationAdmin)