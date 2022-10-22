from django.db import models

# Create your models here.
class Department(models.Model):
    """" 部门表"""
    title = models.CharField(max_length=32,verbose_name="部门标题")
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """" 员工表 """
    name = models.CharField(verbose_name="姓名",max_length=16)
    password = models.CharField(verbose_name="密码",max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    #max_digits表示account最多十位，decimal_places表示小数为2位
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2,default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")

    depart = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",on_delete=models.CASCADE)

    gender_choice = (
        (1,"男"),
        (2,"女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choice)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="电话",max_length=32)
    #想要允许为空，需要加上null=Ture  blank=True
    price = models.IntegerField(verbose_name="价格",default=0)

    level_choice = (
        (1,'高'),
        (2,'中'),
        (3,'低'),
    )
    level = models.SmallIntegerField(verbose_name="级别",choices=level_choice,default=1)

    status_choice = (
        (1,'已占用'),
        (2,'未占用'),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=2)

class Admin(models.Model):
    """管理员表"""
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=64,verbose_name="密码")

    def __str__(self):
        return self.username

class Order(models.Model):
    """订单表"""
    oid = models.CharField(verbose_name="订单号",max_length=64)
    title = models.CharField(verbose_name="名称",max_length=32)
    price = models.IntegerField(verbose_name="价格")

    status_choice = (
        (1,"待支付"),
        (2,"已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态",choices=status_choice,default=1)
    admin = models.ForeignKey(to="Admin",to_field="id",verbose_name="管理员",on_delete=models.CASCADE)