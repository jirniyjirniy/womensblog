from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title='Главная Страница')
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)

def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', context={
        'title': 'Страница о нас',
        'menu': menu,
        'page_obj': page_obj,
    })

class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title='Категория - ' + str(context['posts'][0].cat),
                                       cat_selected=context['posts'][0].cat_id)
        return dict(list(context.items()) + list(c_def.items()))


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    login_url = reverse_lazy('login')
    raise_exception = True
    # success_url = reverse_lazy('home') возвращает на главную

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title='Добовление статьи')
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return render(request, 'women/about.html')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/signin.html'

    def get_context_data(self,object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self,object_list=None ,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_contexnt(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')