from django.db import models


# 患者表
class Patient(models.Model):
    phone = models.CharField(u'患者电话', max_length=11)
    password = models.CharField(u'患者密码', max_length=30)
    name = models.CharField(u'患者姓名', max_length=10)
    sex = models.CharField(u'患者性别', max_length=1)
    age = models.CharField(u'患者年龄', max_length=3)

    class Meta:
        verbose_name = '患者'
        verbose_name_plural = '患者列表'

    def __str__(self):
        return self.name


# 科室表
class Department(models.Model):
    name = models.CharField(u'科室名字', max_length=10)
    address = models.CharField(u'科室地址', max_length=30)

    class Meta:
        verbose_name = '科室'
        verbose_name_plural = '科室列表'

    def __str__(self):
        return self.name


# 医生表
class Doctor(models.Model):
    phone = models.CharField(u'医生电话', max_length=11)
    password = models.CharField(u'医生密码', max_length=30)
    name = models.CharField(u'医生姓名', max_length=10)
    sex = models.CharField(u'医生性别', max_length=1)
    age = models.CharField(u'医生年龄', max_length=3)
    img = models.ImageField(u'医生照片', upload_to='doctorimages/')
    level = models.CharField(u'职位等级', max_length=10)
    description = models.CharField(u'详细描述', max_length=50)
    registration_price = models.IntegerField(u'挂号价格')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="科室")

    def getDepartment(self):
        return Department.objects.get(id=self.department)

    class Meta:
        verbose_name = '医生'
        verbose_name_plural = '医生列表'

    def __str__(self):
        return self.name


# 预约时间表
class TimeNumber(models.Model):
    eight = models.PositiveSmallIntegerField(u'八点可预约人数')
    nine = models.PositiveSmallIntegerField(u'九点可预约人数')
    ten = models.PositiveSmallIntegerField(u'十点可预约人数')
    eleven = models.PositiveSmallIntegerField(u'十一点可预约人数')
    fourteen = models.PositiveSmallIntegerField(u'十四点可预约人数')
    fifteen = models.PositiveSmallIntegerField(u'十五点可预约人数')
    sixteen = models.PositiveSmallIntegerField(u'十六点可预约人数')
    seventeen = models.PositiveSmallIntegerField(u'十七点可预约人数')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="医生")
    default_number = models.PositiveSmallIntegerField(u'默认一个时间点可预约人数')

    def allNumberSetDefault(self):
        '''每天晚上0点可以调用此方法重置可预约人数'''
        self.eight = self.default_number
        self.nine = self.default_number
        self.ten = self.default_number
        self.eleven = self.default_number
        self.fourteen = self.default_number
        self.fifteen = self.default_number
        self.sixteen = self.default_number
        self.seventeen = self.default_number

    class Meta:
        verbose_name = '某时间点可预约人数'
        verbose_name_plural = '某时间点可预约人数列表'


# 预约挂号信息表
class Register(models.Model):
    # 模型字段
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name='患者姓名')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='医生姓名')
    registration_time = models.DateTimeField(u'挂号时间')
    consultation_hours = models.DateTimeField(u'会诊时间')
    illness = models.CharField(u'病情概要', max_length=50)
    address = models.CharField(u'会诊地址', max_length=30)
    out_trade_num = models.UUIDField(u'商户订单号')
    status = models.CharField(u'状态', max_length=10, default='待支付')
    payway = models.CharField(u'支付方式', max_length=10, default='alipay')

    def getPatient(self):
        return Patient.objects.get(id=self.patient)

    def getDoctor(self):
        return Doctor.objects.get(id=self.doctor)

    class Meta:
        verbose_name = '挂号单'
        verbose_name_plural = '挂号单列表'

    def __str__(self):
        # 返回字符串类型的值
        return f'Register {self.id} - {self.patient.name} - {self.doctor.name}'


# 患者评价医生模型
class DoctorEvaluation(models.Model):
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, verbose_name='患者姓名')
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, verbose_name='医生姓名')
    registration = models.OneToOneField('Register', on_delete=models.CASCADE, verbose_name='挂号单', null=True, blank=True, unique=True)
    service_attitude = models.IntegerField(verbose_name='服务态度评分', choices=[(i, str(i)) for i in range(1, 6)])
    professional_level = models.IntegerField(verbose_name='专业水平评分', choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(verbose_name='评价内容', blank=True, null=True)
    evaluation_time = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')

    class Meta:
        verbose_name = '医生评价'
        verbose_name_plural = '医生评价列表'

    def __str__(self):
        return f'{self.patient.name} 对 {self.doctor.name} 的评价'



# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser
