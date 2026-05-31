from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog
from .models import Category , Comment
from django.db.models import Q
from django.contrib.auth.models import User
from django.template.context_processors import request
# Create your views here.

def post_by_category(request , category_id):
    # fetch the post that belongs to the category with the id category_id
    posts = Blog.objects.filter(status = 'Published' , category = category_id)
    try:
        category = Category.objects.get(pk = category_id)
    except:
        # when category not present then redirect user to home page
        return redirect ('home')
        
    # category = get_object_or_404(Category,pk=category_id)
    context = {
        'posts': posts,
        'category' : category
    }
    return render(request,'posts_by_category.html',context)


def blog_detail(request , slug):
    post = get_object_or_404(Blog , slug = slug , status = 'Published')

    if request.method == 'POST':
        comment = Comment()
        comment.user = request.user
        comment.blog = post
        comment.comment = request.POST['comment'] ## ['comment'] from html name attribute where we wrote input of comment.
        comment.save()
        return HttpResponseRedirect(request.path_info)
    #fetch comments from the db for a spesific blog posts--
    comments = Comment.objects.filter(blog = post)
    comment_count = comments.count()
    # print(comments)
    context = {
        'post':post,
        'comments':comments,
        'comment_count':comment_count
    }
    return render(request, 'blog_detail.html', context)



def search(request):
    search = request.GET.get('search')

    blogs = Blog.objects.filter(status='Published')

    if search:
        blogs = blogs.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(blog_body__icontains=search)
        )

    context = {
        'blogs': blogs,
        'search': search,
    }
    return render(request, 'search.html', context)