from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Category,Blog
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.template.context_processors import request
from .forms import CategoryForm , BlogForm , AddUserForm , EditUserForm
from django.contrib.auth.models import User
from blog.models import Comment


# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blog_count = Blog.objects.all().count()
    comment_count = Comment.objects.all().count()

    context = {
        'category_count':category_count,
        'blog_count':blog_count,
        'comment_count':comment_count,
        'recent_posts': Blog.objects.order_by('-created_at')[:5],
        # Charts ke liye — optional
        'monthly_posts': [8, 12, 7, 15, 10, 14],  # real data se replace karo
        'cat_labels': list(Category.objects.values_list('category_name', flat=True)),
        'cat_data':   [Blog.objects.filter(category=c).count() for c in Category.objects.all()],
    }
    return render(request , 'dashboard/dashboard.html',context)



#* show all category to the html page-

def categories(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/categories.html',{'categories':categories})


#* Add new category ---

def add_category(request):
    if request.method == 'POST':
        forms = CategoryForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('categories')
    forms = CategoryForm()
    context = {
        'forms':forms,
    }
    return render (request,'dashboard/add_category.html',context)


def edit_category(request , pk):
    category = get_object_or_404(Category , pk=pk)
    if request.method == 'POST':
        forms = CategoryForm(request.POST , instance=category)
        if forms.is_valid():
            forms.save()
            return redirect('categories')
    forms = CategoryForm( instance=category)
    context = {
        'forms':forms,
        'category':category,
    }
    return render (request,'dashboard/edit_category.html',context)


def delete_category(request , pk ):
    category = get_object_or_404(Category , pk=pk)
    category.delete()
    return redirect('categories')


#*           POST CRUD FUNCTIONALITY

def posts(request):
    posts = Blog.objects.all()
    return render (request, 'dashboard/all_posts.html', {'posts':posts})

def add_post(request):
    if request.method == 'POST':
        forms = BlogForm(request.POST , request.FILES)
        if forms.is_valid():
            post = forms.save(commit=False)  # temporarily saving the form
            post.author = request.user
            post.save()
            title = forms.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect( 'posts' )
        else:
            print("form is invalid")
            print(forms.errors)
    forms = BlogForm()
    context = {
        'forms':forms,
    }
    return render(request, 'dashboard/add_post.html',context)


def edit_post(request , pk ):
    post = get_object_or_404(Blog , pk=pk)
    if request.method == 'POST':
        forms = BlogForm(request.POST , request.FILES , instance=post)
        if forms.is_valid():
            post = forms.save()
            title = forms.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()
            return redirect('posts')
    forms = BlogForm(instance=post )
    context = {
        'forms' : forms,
        'post' : post
    }
    return render(request, 'dashboard/edit_post.html',context)

def delete_post(request , pk):
    post = get_object_or_404(Blog , pk =pk ) 
    # if request.method == 'POST':
    #     post.delete()
    #     return redirect('posts')
    # return render (request,'dashboard/delete_post.html')
    post.delete()
    return redirect ('posts')


#*    users  for manager

def users(request):
    users = User.objects.all()
    return render (request,'dashboard/user.html' , {'users':users})

def add_user(request):
    if request.method == 'POST':
        forms = AddUserForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('users')
        else:
            print(forms.errors)
    forms = AddUserForm()
    context = {
        'forms':forms,
    }
    return render(request,'dashboard/add_user.html',context)


def edit_user(request, pk):
    user = get_object_or_404(User , pk=pk)
    if request.method == 'POST':
        forms = EditUserForm(request.POST , instance=user)
        if forms.is_valid():
            forms.save()
            return redirect('users')
    forms = EditUserForm(instance = user)
    context = {
        'forms':forms,
    }
    return render(request, 'dashboard/edit_user.html',context)


def delete_user(request , pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')