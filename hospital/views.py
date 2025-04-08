import datetime
import uuid
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from .models import *
import re


# 01选择身份登录
class ChooseLoginView(View):
    def get(self, request):
        return render(request, 'chooselogin.html')


# 02患者登录
class PatientLoginView(View):
    def get(self, request):
        return render(request, 'patientlogin.html', {'error': ''})

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        if not phone or not password:
            error = "请输入账号和密码"
            return render(request, 'patientlogin.html', {'error': error})
        patient_list = Patient.objects.filter(phone=phone, password=password)
        if patient_list:
            request.session.clear()
            request.session['patient'] = patient_list[0].name
            # 存入手机号到 session
            request.session['patient_phone'] = phone
            return HttpResponseRedirect("/patientcenter/")
        else:
            error = "账号或密码错误"
            return render(request, 'patientlogin.html', {'error': error})


# 03医生登录
class DoctorLoginView(View):
    def get(self, request):
        return render(request, 'doctorlogin.html', {'error': ''})

    def post(self, request):
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')

        if not phone or not password:
            error = "请输入账号和密码"
            return render(request, 'doctorlogin.html', {'error': error})

        doctor_list = Doctor.objects.filter(phone=phone, password=password)
        if doctor_list:
            request.session['doctor'] = doctor_list[0].name
            request.session['doctor_image'] = str(doctor_list[0].img)
            # 修改重定向路径到医生中心
            return redirect('/doctorcenter/')  # 重点修改这里
        else:
            error = "账号或密码错误"
            return render(request, 'doctorlogin.html', {'error': error})

# 04患者注册
class PatientRegisterView(View):
    def get(self, request):
        return render(request, 'patientregister.html')

    def post(self, request):
        # 只能注册患者账号 医生账号只能由管理员添加
        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        name = request.POST.get('name', '')
        sex = request.POST.get('sex', '')
        age = request.POST.get('age', '')

        # 检查所有字段是否为空
        if not phone or not password or not confirm_password or not name or not sex or not age:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*请填写所有字段"})

        # 验证手机号格式
        phoneRegex = re.compile(r'^1[3-9]\d{9}$')
        if not phoneRegex.match(phone):
            return render(request, 'patientregister.html', {"err": 1, "tips": "*请输入有效的手机号码"})

        # 验证密码长度
        if len(password) < 6:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*密码长度不能少于6位"})

        # 验证两次密码是否一致
        if password != confirm_password:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*两次输入的密码不一致，请重新输入"})

        patientlist = Patient.objects.filter(phone=phone)
        if patientlist:
            return render(request, 'patientregister.html', {"err": 1, "tips": "*该号码已经被注册"})

        patient = Patient.objects.create(phone=phone, password=password, name=name, sex=sex, age=age)
        if patient:
            return HttpResponseRedirect("/patientlogin/")
        return HttpResponseRedirect("/patientregister/")


# 05患者界面
class PatientCenterView(View):
    def get(self, request):
        # 获取 session 中的手机号
        phone = request.session.get('patient_phone', '')
        if not phone:
            return redirect('/patientlogin/')  # 如果患者未登录，重定向到登录页面
        # 根据手机号查询患者信息
        patient = Patient.objects.filter(phone=phone).first()
        print(f"Patient: {patient}")  # 添加调试信息
        if patient is None:
            # 处理患者信息不存在的情况
            return redirect('/patientlogin/')
        patient_name = patient.name
        return render(request, 'patientcenter.html', {'patient_name': patient_name})


# 06选择科室
class ChooseDepartmentView(View):
    def get(self, request):
        department_list = Department.objects.filter().all()
        return render(request, 'choosedepartment.html', {'all_department_list': department_list})


# 07选择医生和时间
class ChooseDoctorAndTimeView(View):
    def get(self, request, department_id):
        department_id = int(department_id)
        department_name = Department.objects.get(id=department_id).name  # 科室名字
        doctor_list = Doctor.objects.filter(department_id=department_id)  # 当前科室里的医生
        doctor_time_number_list = []  # 此医生及其的可预约时间和人数列表
        for doctor in doctor_list:
            doctor_id = doctor.id
            time_number = TimeNumber.objects.filter(doctor_id=doctor_id).first()
            doctor_time_number_list.append([doctor, time_number])

        # 生成最近 7 天的日期列表
        date_list = []
        for i in range(7):
            date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            date_list.append(date)

        # 获取患者选择的日期，如果没有选择则默认为今天
        selected_date = request.GET.get('date', datetime.datetime.now().strftime("%Y-%m-%d"))

        # 定义时间列表
        time_list = ['08', '09', '10', '11', '14', '15', '16', '17']

        # 获取当前时间
        now = datetime.datetime.now()

        return render(request, 'choosedoctorandtime.html',
                      {'department_name': department_name, 'doctor_time_number_list': doctor_time_number_list,
                       'department_id': department_id, 'date_list': date_list, 'selected_date': selected_date,
                       'time_list': time_list, 'now': now})

# 08确认挂号信息预约
class ConfirmRegistrationView(View):
    def get(self, request, department_id, doctor_id, consultation_date, consultation_hours):
        time_number = TimeNumber.objects.filter(doctor_id=doctor_id).first()
        hour = consultation_hours[:2]
        if hour == '08' and time_number.eight == 0:
            return
        elif hour == '09' and time_number.nine == 0:
            return
        elif hour == '10' and time_number.ten == 0:
            return
        elif hour == '11' and time_number.eleven == 0:
            return
        elif hour == '14' and time_number.fourteen == 0:
            return
        elif hour == '15' and time_number.fifteen == 0:
            return
        elif hour == '16' and time_number.sixteen == 0:
            return
        elif hour == '17' and time_number.seventeen == 0:
            return

        department_id = int(department_id)
        doctor_id = int(doctor_id)
        patient = request.session.get('patient', '')
        doctor = Doctor.objects.get(id=doctor_id)
        department = Department.objects.get(id=department_id)
        patient_name = patient
        doctor_name = doctor
        registration_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consultation_hours = f"{consultation_date} {consultation_hours}"
        patient_id = Patient.objects.filter(name=patient).first().id
        address = department.address
        registration_price = doctor.registration_price

        return render(request, 'confirmregistration.html', {'patient_name': patient_name, 'doctor_name': doctor_name,
                                                            'registration_time': registration_time,
                                                            'consultation_hours': consultation_hours,
                                                            'doctor_id': doctor_id, 'patient_id': patient_id,
                                                            'address': address,
                                                            'registration_price': registration_price})

    # 确定预约并支付
    def post(self, request):
        registration_time = request.POST.get('registration_time', '')
        consultation_hours = request.POST.get('consultation_hours', '')
        illness = request.POST.get('illness', '')
        doctor_id = request.POST.get('doctor_id', '')
        patient_id = request.POST.get('patient_id', '')
        address = request.POST.get('address', '')
        out_trade_num = uuid.uuid4().hex
        payway = '支付宝'
        status = '已支付，未检查'
        # 只检查状态为 '已支付，未检查' 的预约
        register = Register.objects.filter(consultation_hours=consultation_hours, patient_id=patient_id, status='已支付，未检查')
        if register:
            return render(request, 'confirmregistration.html', {'message': "支付失败,您已经预约了此时间段！"})
        else:
            Register.objects.create(registration_time=registration_time,
                                    consultation_hours=consultation_hours, illness=illness, doctor_id=doctor_id,
                                    patient_id=patient_id, address=address, out_trade_num=out_trade_num,
                                    payway=payway, status=status)
            time_number = TimeNumber.objects.filter(doctor_id=doctor_id).first()
            hour = consultation_hours[11:13]
            if hour == '08':
                time_number.eight = time_number.eight - 1
            elif hour == '09':
                time_number.nine = time_number.nine - 1
            elif hour == '10':
                time_number.ten = time_number.ten - 1
            elif hour == '11':
                time_number.eleven = time_number.eleven - 1
            elif hour == '14':
                time_number.fourteen = time_number.fourteen - 1
            elif hour == '15':
                time_number.fifteen = time_number.fifteen - 1
            elif hour == '16':
                time_number.sixteen = time_number.sixteen - 1
            elif hour == '17':
                time_number.seventeen = time_number.seventeen - 1
            time_number.save()
            return render(request, 'confirmregistration.html', {'message': "支付成功,完成预约！"})


# 09患者查看预约信息
class PatientShowRegistrationView(View):
    def get(self, request):
        patient = request.session.get('patient')
        if not patient:
            return redirect('/patientlogin/')

        patient = Patient.objects.filter(name=patient).first()
        if not patient:
            return redirect('/patientlogin/')

        register_list = patient.register_set.all()

        # 检查是否有预约记录
        if not register_list:
            message = "暂无预约记录。"
        else:
            message = ""

        return render(request, 'patientshowregistration.html', {'register_list': register_list, 'message': message})


# 10医生界面
class DoctorCenterView(View):
    def get(self, request):
        doctor = request.session.get('doctor', '')
        doctor_image = request.session.get('doctor_image', '')
        return render(request, 'doctorcenter.html', {'doctor_name': doctor, 'doctor_image': doctor_image})


# 11医生展示挂号信息
class DoctorShowRegistrationView(View):
    def get(self, request):
        doctor_name = request.session.get('doctor')
        if not doctor_name:
            return redirect('/doctorlogin/')

        doctor = Doctor.objects.filter(name=doctor_name).first()
        if not doctor:
            return redirect('/doctorlogin/')

        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(status='已支付，未检查').all()
        except Exception as e:
            print(e)
            register_list = []

        # 检查是否有预约
        if not register_list:
            message = "暂无患者预约信息。"
        else:
            message = ""

        return render(request, 'doctorshowregistration.html',
                      {'register_list': register_list, 'doctor_image': doctor.img, 'message': message})

    # 医生确认检查完毕
    def post(self, request):
        register_id = request.POST.get('register_id', '')
        register = Register.objects.get(id=register_id)
        register.status = '已检查'
        print(register.consultation_hours)
        consultation_hours = str(register.consultation_hours)[11:13]
        register.save()
        doctor = request.session.get('doctor')
        doctor = Doctor.objects.filter(name=doctor).first()
        time_number = TimeNumber.objects.filter(doctor_id=doctor.id).first()
        if consultation_hours == '08':
            time_number.eight = time_number.eight + 1
        elif consultation_hours == '09':
            time_number.nine = time_number.nine + 1
        elif consultation_hours == '10':
            time_number.ten = time_number.ten + 1
        elif consultation_hours == '11':
            time_number.eleven = time_number.eleven + 1
        elif consultation_hours == '14':
            time_number.fourteen = time_number.fourteen + 1
        elif consultation_hours == '15':
            time_number.fifteen = time_number.fifteen + 1
        elif consultation_hours == '16':
            time_number.sixteen = time_number.sixteen + 1
        elif consultation_hours == '17':
            time_number.seventeen = time_number.seventeen + 1
        time_number.save()

        try:
            register_list = doctor.register_set.order_by('consultation_hours').filter(status='已支付，未检查').all()
        except Exception as e:
            print(e)
            register_list = []

        return render(request, 'doctorshowregistration.html', {'register_list': register_list, 'doctor_image': doctor.img})

# 患者信息修改
class PatientUpdateInfoView(View):
    def get(self, request):
        # 获取 session 中的手机号
        phone = request.session.get('patient_phone', '')
        if not phone:
            return redirect('/patientlogin/')  # 如果患者未登录，重定向到登录页面
        # 根据手机号查询患者信息
        patient = Patient.objects.filter(phone=phone).first()
        return render(request, 'patientupdateinfo.html', {'patient': patient})

    def post(self, request):
        patient_id = request.POST.get('patient_id')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return redirect('/patientlogin/')  # 如果患者不存在，重定向到登录页面

        phone = request.POST.get('phone', '')
        password = request.POST.get('password', '')
        name = request.POST.get('name', '')
        sex = request.POST.get('sex', '')
        age = request.POST.get('age', '')

        # 检查所有字段是否为空
        if not phone or not name or not sex or not age:
            return render(request, 'patientupdateinfo.html', {'patient': patient, 'error': '请填写所有必填字段'})

        # 验证手机号格式
        phoneRegex = re.compile(r'^1[3-9]\d{9}$')
        if not phoneRegex.match(phone):
            return render(request, 'patientupdateinfo.html', {'patient': patient, 'error': '请输入有效的手机号码'})

        # 验证密码长度
        if password and len(password) < 6:
            return render(request, 'patientupdateinfo.html', {'patient': patient, 'error': '密码长度不能少于6位'})

        # 检查手机号是否重复
        if phone != patient.phone and Patient.objects.filter(phone=phone).exists():
            return render(request, 'patientupdateinfo.html', {'patient': patient, 'error': '该手机号码已被注册，请使用其他号码'})

        # 更新患者信息
        patient.phone = phone
        if password:
            patient.password = password
        patient.name = name
        patient.sex = sex
        patient.age = age
        patient.save()

        # 更新 session 中的手机号
        request.session['patient_phone'] = phone

        return redirect('/patientcenter/')

# 评价医生
class EvaluateDoctorView(View):
    def get(self, request, register_id):
        register = get_object_or_404(Register, id=register_id)
        patient = request.session.get('patient')
        patient = Patient.objects.filter(name=patient).first()
        rating_range = range(1, 6)  # 生成评分范围列表

        try:
            DoctorEvaluation.objects.get(registration=register)
            register.has_evaluation = True
        except DoctorEvaluation.DoesNotExist:
            register.has_evaluation = False

        return render(request, 'evaluate_doctor.html', {'register': register, 'rating_range': rating_range})

    def post(self, request, register_id):
        register = get_object_or_404(Register, id=register_id)
        patient = request.session.get('patient')
        patient = Patient.objects.filter(name=patient).first()
        rating_range = range(1, 6)  # 生成评分范围列表

        service_attitude = request.POST.get('service_attitude')
        professional_level = request.POST.get('professional_level')
        comment = request.POST.get('comment')

        # 验证评分是否有效
        if not service_attitude or not professional_level:
            messages.error(request, '请选择服务态度和专业水平评分！')
            return render(request, 'evaluate_doctor.html', {'register': register, 'rating_range': rating_range})

        DoctorEvaluation.objects.create(
            patient=patient,
            doctor=register.doctor,
            registration=register,
            service_attitude=service_attitude,
            professional_level=professional_level,
            comment=comment
        )

        messages.success(request, '评价提交成功！')
        return redirect('patientcenter')

# 患者评价记录
class PatientEvaluationRecordsView(View):
    def get(self, request):
        patient = request.session.get('patient')
        if not patient:
            return redirect('/patientlogin/')

        patient = Patient.objects.filter(name=patient).first()
        if not patient:
            return redirect('/patientlogin/')

        register_list = Register.objects.filter(patient=patient, status='已检查')

        # 检查是否有评价信息
        if not register_list:
            message = "暂无医生评价信息。"
        else:
            message = ""

        for register in register_list:
            evaluation_exists = DoctorEvaluation.objects.filter(registration=register).exists()
            register.has_evaluation = evaluation_exists

        return render(request, 'patient_evaluation_records.html', {'register_list': register_list, 'message': message})


# 医生查看患者评价
class DoctorViewPatientEvaluationsView(View):
    def get(self, request):
        doctor_name = request.session.get('doctor')
        if not doctor_name:
            return redirect('/doctorlogin/')

        doctor = Doctor.objects.filter(name=doctor_name).first()
        if not doctor:
            return redirect('/doctorlogin/')

        evaluations = DoctorEvaluation.objects.filter(registration__doctor=doctor)

        # 检查是否有评价记录
        if not evaluations:
            message = "暂无患者评价记录。"
        else:
            message = ""

        return render(request, 'doctor_view_patient_evaluations.html', {'evaluations': evaluations, 'message': message})

# 医生个人信息的展示
class DoctorInfoView(View):
    def get(self, request):
        doctor_name = request.session.get('doctor', '')
        doctor = Doctor.objects.filter(name=doctor_name).first()
        if doctor:
            return render(request, 'doctorinfo.html', {'doctor': doctor})
        return redirect('/doctorlogin/')

# 显示已预约信息和处理取消预约请求
class PatientCancelRegistrationView(View):
    def get(self, request):
        phone = request.session.get('patient_phone', '')
        if not phone:
            return redirect('/patientlogin/')

        patient = Patient.objects.filter(phone=phone).first()
        if patient is None:
            return redirect('/patientlogin/')

        register_list = patient.register_set.order_by('consultation_hours').filter(status='已支付，未检查').all()

        # 检查是否有可取消的预约
        if not register_list:
            message = "暂无可取消的预约信息。"
        else:
            message = ""

        return render(request, 'patientcancelregistration.html', {'register_list': register_list, 'message': message})


    def post(self, request, register_id):
        register = Register.objects.get(id=register_id)
        register.status = '已取消'
        register.save()
        consultation_hours = str(register.consultation_hours)[11:13]
        doctor = register.doctor
        time_number = TimeNumber.objects.filter(doctor_id=doctor.id).first()
        if consultation_hours == '08':
            time_number.eight = time_number.eight + 1
        elif consultation_hours == '09':
            time_number.nine = time_number.nine + 1
        elif consultation_hours == '10':
            time_number.ten = time_number.ten + 1
        elif consultation_hours == '11':
            time_number.eleven = time_number.eleven + 1
        elif consultation_hours == '14':
            time_number.fourteen = time_number.fourteen + 1
        elif consultation_hours == '15':
            time_number.fifteen = time_number.fifteen + 1
        elif consultation_hours == '16':
            time_number.sixteen = time_number.sixteen + 1
        elif consultation_hours == '17':
            time_number.seventeen = time_number.seventeen + 1
        time_number.save()
        return redirect('/patientcancelregistration/')

# 健康小贴士视图
class HealthTipsView(View):
    def get(self, request):
        return render(request, 'healthtips.html')