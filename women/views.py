from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import *

menu = [{'title': 'О сайте', 'url_name': 'about'},
        {'title': 'Добавить статью', 'url_name': 'add_page'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        {'title': 'Войти', 'url_name': 'login'}
        ]

def index(request):
    post = Women.objects.all()
    return render(request, 'women/index.html', context={
        'title': 'Главная Страница',
        'menu': menu,
        'posts': post,
        'cat_selected': 0,
    })

def about(request):
    return render(request, 'women/about.html', context={
        'title': 'Страница о нас',
        'menu': menu,
    })

def show_category(request, cat_id):
    post = Women.objects.filter(cat_id=cat_id)
    cats = Category.objects.all()

    if len(post) == 0:
        raise Http404()

    context = {
        'title': 'Отображение по рубрикм',
        'menu': menu,
        'posts': post,
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=context)

def addpage(request):
    return HttpResponse('Добавление статьи')

def contact(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def show_post(request, post_id):
    post = get_object_or_404(Women, pk=post_id)

    return render(request, 'women/post.html', context={
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    })

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')