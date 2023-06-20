from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy

# Create your views here.

from .models import *
from .forms import *
from .utils import DataMixin

menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Додати статтю', 'url_name': 'addpage'},
        {'title': 'Зворотній зв\'язок', 'url_name': 'contact'},
        {'title': 'Увійти', 'url_name': 'login'},
        ]


class MovieHome(DataMixin, ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Головна сторінка')
        context = dict(list(context.items()) + list(c_def.items()))
        return context
        # cats = Category.objects.all()
        # context['title'] = 'Головна сторінка'
        # context['menu'] = menu
        # context['cats'] = cats
        # context['cat_selected'] = 0

    def get_queryset(self):
        return Movie.objects.filter(is_published=True).select_related('cat')


# def index(requests):
#     posts = Movie.objects.all()
#     cats = Category.objects.all()
#     context = {'menu': menu,
#                'cats': cats,
#                'title': 'Головна сторінка',
#                'cat_selected': 0,
#                'posts': posts
#                }

# return render(requests, 'movies/index.html', context=context)

def about(requests):
    contact_list = Movie.objects.all()
    paginator = Paginator(contact_list, 3)
    page_number = requests.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(requests, 'movies/about.html', {'menu': menu,
                                                  'title': 'Про сайт',
                                                  'page_obj': page_obj})


# def addpage(requests):
#     return HttpResponse('Додавання статті')

def contact(requests):
    return HttpResponse('Зворотній зв\'язок')


# def login(requests):
#     return HttpResponse('Авторизація')

# def show_post(requests, post_slug):
#     post = get_object_or_404(Movie, slug=post_slug)
#     context = {'menu': menu,
#                'post': post,
#                'title': post.title,
#                'cat_selected': post.cat_id
#                }
#     return render(requests, 'movies/post.html', context=context)
#
#
#
# def categories(requests, cat_id):
#     return HttpResponse(f'<h1>Фільми по категоріях</h1>{cat_id}')

# def show_category(requests, cat_id):
#     posts = Movie.objects.filter(cat_id=cat_id)
#     cats = Category.objects.all()
#     context = {'menu': menu,
#                'cats': cats,
#                'title': '',
#                'cat_selected': cat_id,
#                'posts': posts
#                }
#
#
#     return render(requests, 'movies/index.html', context=context)

# def addpage(requests):
#     if requests.method == 'POST':
#         form = AddPostForm(requests.POST, requests.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             form.save()
#             # Movie.objects.create(**form.cleaned_data)
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#         context = {'form': form, 'menu': menu, 'title': 'Додавання статті'}
#     return render(requests, 'movies/addpage.html', context=context)

# def pageNotFound(requests):
#     return HttpResponseNotFound('<h2>Сторінку не знайдено</h2>')


class MovieCategory(DataMixin, ListView):
    model = Movie
    template_name = 'movies/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Movie.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Категорія - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        context = dict(list(context.items()) + list(c_def.items()))
        return context
        # context['title'] = 'Категорія - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # context['cats'] = cats
        # context['cat_selected'] = 0
        # return context


class ShowPost(DataMixin, DetailView):
    model = Movie
    template_name = 'movies/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'movies/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Додавання статті')
        context = dict(list(context.items()) + list(c_def.items()))
        return context


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'movies/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Реєстрація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

#
# class LoginUser(DataMixin, LoginView):
#     form_class = LoginUserForm
#     template_name = 'movies/login.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Авторизація')
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context
#
#     def get_success_url(self):
#         return reverse_lazy('home')

# MTV - патерн: Models Views Templates
# ORM -
# T - Templates

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'movies/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизація')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_success_url(self):
        return reverse_lazy('home')
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'movies/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Зворотній зв\'зок')
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# @cache
def logout_user(request):
    logout(request)
    return redirect('login')