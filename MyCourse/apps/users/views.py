# encoding=utf8
from django.shortcuts import render
# 导入Django自己的验证和登录方法
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile,EmailVerifyRecoed
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from .forms import LoginForms,RegisterForm,ForgetForm,ModifyPwdForm
from utils.email_send import send_register_email
# Create your views here.


# 重置他的authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        # 利用Q对象来匹配username或者是email
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            # 去比较查出来的user的密码
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 用户点击邮箱的激活类
class ActivUserView(View):

    def get(self,request,active_code):
        all_recodes = EmailVerifyRecoed.objects.filter(code = active_code)
        # 查询出来的就是列表中嵌套字典
        if all_recodes:
            for recode in all_recodes:
                email = recode.email
                user = UserProfile.objects.get(email = email)
                user.is_active = True
                user.save()
        # 当用户的输入的激活连接失效的时候就返回这个连接失效的页面
        else:
            return render(request,"active_fail.html")
        return render(request,"login.html")


# 密码重置view因为用户点击的连接中是有code的但是from表单提交时是没有code所以就分别写了一个get的和post的
class ResetUserView(View):
    def get(self,request,active_code):
        all_recode = EmailVerifyRecoed.objects.filter(code = active_code)
        if all_recode:
            for recode in all_recode:
                email = recode.email
                return render(request,"password_reset.html",{"email":email})


# 密码重置view因为用户点击的连接中是有code的但是from表单提交时是没有code所以就分别写了一个get的和post的
class ModifyPwdView(View):

    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)

        if modify_form.is_valid():
            pwd1 = request.POST.get("password1","")
            pwd2 = request.POST.get("password2","")
            email = request.POST.get("email","")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email,"msg":"密码不一致!"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request,"login.html",{})
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 注册的view类
class RegisterView(View):

    def get(self,request):
        register_form = RegisterForm()
        return render(request,"register.html",{"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email',"")
            if UserProfile.objects.filter(email = user_name):
                # 拿到用户输入的用户名去向数据库中的email进行比较如果重复的话就返回错误信息
                return render(request,"register.html",{"msg":"用户名已经存在","register_form":register_form})
            user_password = request.POST.get('password',"")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 表明用户还没有激活
            user_profile.is_active = False
            # 调用make_password对我们的密码进行加密
            user_profile.password = make_password(user_password)
            user_profile.save()

            # 代用utils下的email_register_send去发送验证码去邮箱
            send_register_email(user_name,"register")

            return render(request,"login.html")
        else:
            return render(request,"register.html",{"register_form":register_form})

            # pass



# 用类来写我们的逻辑这里继承Django的基类View就不需要进行get或这个post的判断了
class LoginView(View):

    def get(self,request):
        return render(request, "login.html", {})

    def post(self,request):
        # 生成实例把post表单传过来的dict给放进去
        login_from = LoginForms(request.POST)
        # 用forms验证成功的话才去去这个post的内容去验证登录
        if login_from.is_valid():
            user_name = request.POST.get('username', "")
            user_password = request.POST.get('password', "")
            user = authenticate(username=user_name, password=user_password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活!"})
            else:
                return render(request,"login.html",{"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_from":login_from})


# 重置我们的authenticate方法之后我们调用的时候就会用我们自己的authenticate方法dbs
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get('username', "")
#         user_password = request.POST.get('password', "")
#         user = authenticate(username=user_name,password=user_password)
#         if user is not None:
#             login(request,user)
#             return render(request,"index.html")
#         else:
#             return render(request,"login.html",{"msg":"用户名或密码错误!"})
#
#     else:
#         return render(request,"login.html",{})


# 忘记密码的view类
class ForGetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,"forgetpwd.html",{"forget_form":forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email","")
            send_register_email(email,'forget')
            return render(request,"send_sucess.html")
        else:
            return render(request,"forgetpwd.html",{"forget_form":forget_form,"msg":"用户名密码!"})