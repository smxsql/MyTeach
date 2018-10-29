# encoding=utf-8
# 进行表单的预处理验证

from django import forms
from captcha.fields import CaptchaField


#  验证登录的表单from
class LoginForms(forms.Form):
    # required=True就是这字段是不能为空的
    username = forms.CharField(required=True)
    # 限制我们的password的长度最少是5这样的话就会减少去数据库查询的负担
    password =forms.CharField(required=True,min_length=5)


# 验证注册的表单from
class RegisterForm(forms.Form):
    # 对我们的email进行按照邮箱的格式验证
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 自定义错误信息:就是在from字段中加上error_messages={"invalid":u"验证码错误"
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})


# 验证找回密码的表单from
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


# 密码找回表单验证
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)