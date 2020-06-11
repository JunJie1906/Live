from . import models,forms
from django.shortcuts import render, redirect

import liveapp.models

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')

    users = models.User.objects.all()
    user_count = len(users)
    curr_live = liveapp.models.Live.objects.all()

    return render(request,'login/index.html',context={'curr_live':curr_live,'user_count':user_count})

def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')
    if request.method=="POST":
        login_form = forms.UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(name=username)
                if user.password!=password:
                    message2 = '密码错误'
                    return render(request, 'login/login.html',locals())
            except:
                message1 = '用户不存在'
                return render(request, 'login/login.html',locals())
            request.session['is_login'] = True
            request.session['user_name'] = user.name

            print(user.name,user.id)
            # request.session['user_id'] = user.id
            return redirect('/index')

    login_form = forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            print(username,password1,password2,email,sex)
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.sex = sex
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/index/")
    request.session.flush()
    return redirect('/index/')
