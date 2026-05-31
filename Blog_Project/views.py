from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from blog.models import Category,Blog
from assignments.models import About , SocialMedia
from .forms import RegistrationForm
from django.contrib import auth
import random

def home(request):
    categories = Category.objects.all()
    categoriesList = list(categories)

    random.shuffle(categoriesList)
    # fearured_post = categoriesList[0] if categoriesList else None
    print(categoriesList, ' Anuj')
    fearured_post = Blog.objects.filter(is_featured = True).order_by('?')
    posts = Blog.objects.filter(is_featured = False , status = 'Published')
    
    # fetch about us 
    try:
        about = About.objects.get()
    except:
        about = None

    #* fetch socialmedia link from assignments models
    
    context = {
        'categories':categories,
        'fearured_post':fearured_post,
        'posts' : posts,
        'about' : about,
        
    }
    return render(request , 'home.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    context = {
        'form' : form,
    }
    return render(request,'register.html',context)
    
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username,password=password)
            if user is not None:
                auth.login(request,user)
            return redirect('home')
    form = AuthenticationForm()
    context = {
        'form':form
    }
    return render (request,'login.html' , context)


def logout(request):
    auth.logout(request)
    return redirect('home')