from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Users, Verification
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login as dj_login
from index.models import Favorites, Videos, get_short_id
from django.core import mail
from django.utils import timezone


# Create your views here.
def login(request):
    '''用户登录界面及处理'''
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.method == 'POST':
        # 变量获取
        user_name = request.POST.get("username", "")
        pwd = request.POST.get("userpassword", "")

        if Users.objects.filter(username=user_name):  # 用户存在
            # 使用内置方法验证
            user = authenticate(username=user_name, password=pwd)
            if user: # 验证通过
                if user.is_active:  # 用户已激活
                    dj_login(request,user)  # 用户登录
                    # messages.error(request, '登录成功')
                    return redirect("/")
                else:  # 用户未激活 
                    messages.error(request, '激活失败')
                    return redirect("/login/")
            else:
                messages.error(request, '用户名和密码不匹配')
                return redirect("/login/")
        else:  # 用户不存在
            messages.error(request, '未找到该用户')
            return redirect('/login/')

def register(request):
    '''用户注册界面'''
    if request.method == "GET":
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 变量获取
        user_name = request.POST.get("username", "")
        email = request.POST.get("useremail","")
        pwd = request.POST.get("userpassword", "")
        confirmpwd = request.POST.get("confirmpassword", "")
        if pwd != confirmpwd:
            messages.error(request, '两次密码不一致')
            return redirect('/login/register/')

        user = Users.objects.filter(email=email)
        if not user:  # 邮箱不存在，可以创建用户
            user = Users.objects.filter(username=user_name)
            if not user:  # 用户名不存在
                Users.objects.create(username=user_name, email=email, password=make_password(pwd)) # 创建用户
                messages.error(request, '用户创建成功')
                return redirect('/login/')
            else:  # 用户存在
                messages.error(request, '用户名已存在')
                return redirect('/login/register/')
        else:  # 邮箱已注册
            messages.error(request, '邮箱已被注册')
            return redirect('/login/')
        
def user_home(request,user_id):
    '''用户个人主页'''
    if request.method == "GET":
        var = {}  # 传递到前端的变量
        current_user = request.user # 获取当前用户
        home_user = Users.objects.filter(id=user_id).get()  # 获取当前主页用户
        favorites = Favorites.objects.filter(user_src=home_user)  # 获取主页用户收藏
        var.update({'favorites':favorites})
        videos = Videos.objects.filter(author=home_user)
        var.update({'videos':videos})

        if home_user:  # 用户存在
            if int(home_user.id) == int(current_user.id):  # 当前用户是该主页用户
                is_user = '1'
                var.update({'is_user':is_user})
            else:  # 当前用户不是该主页用户
                is_user = '0'
                var.update({'is_user':is_user})
        else:  # 用户不存在
            messages.error(request, '用户不存在')
            return redirect('/index/')
        
        var.update({'user':home_user})
        return render(request, 'user_home.html', context=var)
    
    elif request.method == 'POST':
        form_id = request.POST.get("formid",'')
        if form_id == '1':
            # logout()，会清理 session
            logout(request)
            # messages.error(request, '成功登出')
            return redirect('/index/')
        
def send_email(request):
    '''更改密码发送邮件'''
    if request.method == "GET":
        var = {}  # 传递到前端的变量
        return render(request, 'reset_psw.html', context=var)
    elif request.method == 'POST':
        email = request.POST.get("email",'')
        if Users.objects.filter(email = email):  # 用户存在
            # 生成16位验证码
            va1 = get_short_id()
            va2 = get_short_id()
            va = va1 + va2
            # 发送验证码邮件
            subject = "邮箱验证码"
            message = "你的验证码为：\n" + va
            from_email = "asclep@163.com"
            recipient_list = [email,]
            mail.send_mail(subject=subject, from_email=from_email, recipient_list=recipient_list, message=message)
            # 将验证码信息存入库中
            Verification.objects.create(email=email, code=va)
            return redirect('/login/send_email/')
        else:
            var = {}  # 传递到前端的变量
            messages.error(request, '用户不存在')
            return render(request, 'reset_psw.html', context=var)

def psw_rst(request):
    '''更改密码'''
    if request.method == "GET":
        var = {}  # 传递到前端的变量
        return render(request, 'new_psw.html', context=var)
    elif request.method == 'POST':
        # 变量获取
        var = {}  # 传递到前端的变量
        email = request.POST.get("email",'')
        act = request.POST.get("act",'')
        userpassword = request.POST.get("userpassword",'')

        if not Users.objects.filter(email=email):
            messages.error(request, '用户不存在')
            return render(request, 'new_psw.html', context=var)
        else:
            user = Users.objects.filter(email=email).get()
            if not Verification.objects.filter(email=email, code=act):
                messages.error(request, '用户未申请或验证码不正确')
                return render(request, 'new_psw.html', context=var)
            else:
                ver = Verification.objects.filter(email=email, code=act).get()
                now = (timezone.now()-timezone.timedelta(minutes=5))
                if ver.gen_time < now:
                    messages.error(request, '验证码已过期')
                    return render(request, 'new_psw.html', context=var)
                else:
                    user.password = make_password(userpassword)
                    user.save()
                    vers = Verification.objects.filter(gen_time__lt = now).get()
                    vers.delete()
                    messages.error(request, '修改成功,请登录')
                    return redirect('/login/')
