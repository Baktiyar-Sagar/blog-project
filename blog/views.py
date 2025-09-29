from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, PostForm, UpdateProfileForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_list(request):
    categoryQ = request.GET.get('category')
    tagQ = request.GET.get('tag')
    searchQ = request.GET.get('search')

    posts = Post.objects.all()

    if categoryQ:
        posts = posts.filter(category__name = categoryQ)

    if tagQ:
        posts = posts.filter(tag__name = tagQ)

    if searchQ:
        posts = posts.filter(
            Q(title__icontains = searchQ)|
            Q(tag__name__icontains = searchQ)|
            Q(category__name__icontains = searchQ)
        ).distinct()
    # pagination
    paginator = Paginator(posts, 6) # per page 6 post
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {
        'page_object' : page_object,
        'categories' : Category.objects.all(),
        'tags': Tag.objects.all(),
        'search_query': searchQ,
        'category_query': categoryQ,
        'tag_query': tagQ,
    }
    return render(request, 'blog/post_list.html', context)


def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save( commit= False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return redirect('post_details', id= post.id)
    else:
        comment_form = CommentForm()

    comments = post.comment_set.all()
    is_liked = post.liked_users.filter(id= request.user.id).exists()
    like_count = post.liked_users.count()

    context = {
        'post': post,
        'categories': Category.objects.all(),
        'comments': comments,
        'comment_form': comment_form,
        'is_liked': is_liked,
        'like_count': like_count,
    }
    post.view_count +=1 # when ever the page load the view count will increase
    post.save() 

    return render(request, 'blog/post_details.html', context)

@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.liked_users.filter(id= request.user.id):
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)

    return redirect('post_details', id = post.id)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m() # we use this if the form has many to many field 
            return redirect('post_list')
    else: 
        form = PostForm()

        return render(request, 'blog/post_create.html', {'form':form})
    
@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else: 
        form = PostForm(instance=post)

        return render(request, 'blog/post_create.html', {'form':form})
    
@login_required    
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse('profile') + '?section=posts')
    # return redirect('profile')



def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    
    return render(request, 'user/signup.html', {'form' : form})


# Profile page
@login_required
def profile_view(request):
    section = request.GET.get('section', 'profile')
    context = {'section' : section}
    
    if section == 'posts':
        posts = Post.objects.filter(author = request.user)
        context['posts'] = posts 
    
    elif section == 'update':
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile?section=update')
        else:
            form = UpdateProfileForm(instance=request.user)
    
        context['form'] = form
    
    return render(request, 'user/profile.html', context)

