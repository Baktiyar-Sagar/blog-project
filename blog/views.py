from django.shortcuts import render, get_object_or_404
from .models import Post, Category, Tag, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CommentForm, PostForm
from django.db.models import Q
from django.core.paginator import Paginator
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
    paginator = Paginator(posts, 4) # per page 4 post
    page_number = request.GET.get('page')
    page_object = request.get_page(page_number)
    context = {
        'page_object' : page_object,
        'categories' : Category.objects.all(),
        'tags': Tag.objects.all(),
        'search_query': searchQ,
        'category_query': categoryQ,
        'tag_query': tagQ,
    }
    return render(request, '', context)