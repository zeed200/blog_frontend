from django.shortcuts import render, redirect
import requests
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from user.forms import PostCreateForm


# Create your views here.
def post_list(request):
    backend_url = "http://127.0.0.1:8000/"
    headers = {'Content-Type':"application/json"}
    response = requests.get(backend_url,headers=headers)
    posts = response.json()
    tok = request.COOKIES.get("tok")
    page = request.GET.get('page')
    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) 
    
    

    return render(request, 'blog/index.html', {'posts':posts, 'page': page, 'title': 'الصفحة الرئيسية'})



   

def post_detail(request, post_id):
    tok = request.COOKIES.get("tok")
    if tok: 
        headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    else:
      headers = {'Content-Type':"application/json"}
    backend_url = "http://127.0.0.1:8000/detail/"+str(post_id)
    
    response_post = requests.get(backend_url,headers=headers)
    posts = response_post.json()
    response_comments = requests.get("http://127.0.0.1:8000/comment_post/"+str(post_id),headers=headers)
    comments = response_comments.json()
    tok = request.COOKIES.get("tok") 
    
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']
        post = post_id
        data = json.dumps({'name':name, 'email':email, 'body':body, 'post':post})
        response_comment = requests.post("http://127.0.0.1:8000/comment_post/"+str(post_id),headers=headers,data=data)
        return redirect('detail',post_id=post_id)
    
    return render(request, 'blog/detail.html', {'post':posts, 'comments':comments})

def about(request):
    context = {
        'title': 'من أنا',
    }
    return render(request, 'blog/about.html', context)

def Create_Post(request):
    tok = request.COOKIES.get("tok")
    backend_url = "http://127.0.0.1:8000/new_post/"
    headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():   
            title = request.POST['title']
            content = request.POST['content']
           
            data = json.dumps({'title':title, 'content':content})
            requests.post(backend_url,headers=headers,data=data)
            return redirect('home')
    else:
        form = PostCreateForm()

    return render(request, 'blog/new_post.html',{
        'title':'إنشاء تدوينة',
        'form':form,
    })

def Update_Post(request, post_id):
    tok = request.COOKIES.get("tok")
    
    backend_url = "http://127.0.0.1:8000/detail/"+str(post_id)+"/update/"
    headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
    response_post = requests.get(backend_url,headers=headers)
    post = response_post.json()
    if request.method == 'POST':
         title = request.POST.get('title')
         content = request.POST.get('content')
         data = json.dumps({'title':title, 'content':content})   
         status = requests.put(backend_url,headers=headers,data=data)
         if status.ok:
            return redirect('home')
    return render(request, 'blog/post_update.html',{
        'title':'تعديل التدوينة',
        'post':post
    })
def Delete_Post(request, post_id):
     tok = request.COOKIES.get("tok")
     backend_url = "http://127.0.0.1:8000/detail/"+str(post_id)+"/delete/"
     headers = {'Content-Type':"application/json",'Authorization':f"Token {tok}"}
     response_post = requests.get(backend_url,headers=headers)
     post = response_post.json()
     if request.method == 'POST':
         status = requests.delete(backend_url,headers=headers)
         if status.ok:
            return redirect('home')
         
     return render(request, 'blog/post_confirm_delete.html',{
        'title':'حذف التدوينة',
        'post':post
    })
 