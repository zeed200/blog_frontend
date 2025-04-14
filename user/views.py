from django.shortcuts import render, redirect
from .forms import *
import requests
import json
from django.contrib import messages
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import base64
# from django.contrib.auth import authenticate, login, logout
# from blog.models import Post
# from django.contrib.auth.decorators import login_required
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def register(request):    
    backend_url = "http://127.0.0.1:8000/register/"
    headers = {'Content-Type':"application/json"}
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():   
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            data = json.dumps({'username':username, 'email':email, 'first_name':first_name, 'last_name':last_name, 'password1':password1})
            requests.post(backend_url,headers=headers,data=data)
            messages.success(request, f'تهانينا {username} لقد تمت العمليه بنجاح .')
            return redirect('login')
    else:
        form = UserCreationForm()


    return render(request, 'register.html', {
        'title': 'إنشاء حساب',
        'form': form,
    })

def login_user(request):
    backend_url = "http://127.0.0.1:8000/login/"
    headers = {'Content-Type':"application/json"}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
           username = request.POST['username']
           password = request.POST['password']
           data = json.dumps({'username':username, 'password':password})
           status = requests.post(backend_url,headers=headers,data=data)
       
           if status.ok:
               red = redirect('profile')
               key = status.json()
               red.set_cookie("tok",key['token'])   
               return red
           else:
               messages.warning(request, 'هناك خطأ في أسم المستخدم أو كلمة المرور')
           

    else:        
      form = LoginForm()
    return render(request, 'login.html', {
        'title': 'تسجيل الدخول',
        'form': form,
    })

def logout_user(request):
    tok = request.COOKIES.get("tok") 
    
    backend_url = "http://127.0.0.1:8000/logout/"
    headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    status = requests.post(backend_url,headers=headers)
    
   
    response = render(request, 'logout.html', {
        'title': 'تسجيل الخروج',
    })
    response.delete_cookie("tok")
    return response

def profile(request):
    tok = request.COOKIES.get("tok") 
    
    backend_url = "http://127.0.0.1:8000/profile/"
    headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    response = requests.get(backend_url,headers=headers)
    profile = response.json()
  
    post_list = profile['posts']
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'profile.html', {
        'title': 'الملف الشخصي',
        'profile':profile,
        'page': page
        
    })

def profile_update(request):
    tok = request.COOKIES.get("tok") 
    
    backend_url = "http://127.0.0.1:8000/profile_update/"
    headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    response = requests.get(backend_url,headers=headers)
    profile = response.json()

    if request.method == 'POST':
         email = request.POST.get('email')
         first_name = request.POST.get('first_name')
         last_name = request.POST.get('last_name')
         base64 = request.POST.get('base64')
         data = json.dumps({'email':email, 'first_name':first_name, 'last_name':last_name, 'base64':base64})   
         status = requests.put(backend_url,headers=headers,data=data)
         if status.ok:
            messages.success(request, 'لقد تم تحديث الملف الشخصي بنجاح')
            return redirect('profile')

    
   
    context = {
        'title': 'تعديل الملف الشخصي',
        'profile': profile,
       
    }
    return render(request, 'profile_update.html', context)