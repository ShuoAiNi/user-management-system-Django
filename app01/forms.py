from django import forms
from app01.models import UserInfo,PrettyNum,Admin,Order
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from app01.encoding import md5


#利用modelform
class UserModelForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ["name","password","age","account","create_time","gender","depart"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #此时self.fields.items()为元组类型，name为fields中的值，field为其对象
        for name,field in self.fields.items():
           field.widget.attrs = {"class":"form-control","placeholder":field.label}

class PrettyModelForm(forms.ModelForm):
    # #验证方式一: 利用正则表达式对字段进行校验，
    # mobile = forms.CharField(
    #     label="手机号",
    #     validators=[RegexValidator(r'^1[3-9]\d{9}$','手机号格式错误'),]
    # )

    class Meta:
        model = PrettyNum
        fields = ["mobile","price","status","level"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {"class":"form-control","placeholder":field.label}

    #验证方式二: 钩子函数
    def clean_mobile(self):
        moble_text = self.cleaned_data['mobile']
        if len(moble_text) != 11 :
            #验证不通过
            raise ValidationError("手机号格式错误")
        return moble_text

class AdminModel(forms.ModelForm):
    confirm_password = forms.CharField(label="确认密码",widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = Admin
        fields = ["username","password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


    #利用钩子函数对密码进行加密
    def clean_password(self):
        password = self.cleaned_data['password']
        return md5(password)

     # 钩子函数
    def clean_confirm_password(self):
        confirm = md5(self.cleaned_data['confirm_password'])
        password = self.cleaned_data['password']
        if confirm != password:
            raise ValidationError("密码不一致")
        return confirm

#利用form
class LoginForm(forms.Form):
    username = forms.CharField(label="用户名",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"用户名"}))
    password = forms.CharField(label="密码",widget=forms.PasswordInput(attrs={"class":"form-control","placeholder":"密码"},render_value=True))
    code = forms.CharField(label="验证码",widget=forms.TextInput(attrs={"class":"form-control","placeholder":"验证码"}))

    def clean_password(self):
        password = self.cleaned_data["password"]
        return md5(password)


class OrderModelForm(forms.ModelForm):
    class Meta:
        model = Order
        # fields = "__all__"选择所有字段
        exclude = ["oid","admin"] #排除oid字段

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}
