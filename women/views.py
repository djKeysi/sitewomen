from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
      Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

#cats_db = [
 #   {'id': 1, 'name': 'Актрисы'},
  #  {'id': 2, 'name': 'Певицы'},
   # {'id': 3, 'name': 'Спортсменки'},
#]

# def index(request): #HttpRequest
#     # t=render_to_string('women/index_old.html')
#     # return HttpResponse(t)
#
#     #posts = Women.objects.filter(is_published=1)
#     posts = Women.published.all().select_related('cat')
#     #data = {'title': 'главная страница',
#          #   'menu': menu,
#             #'float':24.67,
#             #'url': slugify("The Main Page"),
#            # 'posts':posts,
#             #'cat_selected':0,
#
#           #  }
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#     }
#     return render(request,'women/index.html',context=data)

# class WomenHome(TemplateView):
#     template_name = 'women/index.html'
#
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': Women.published.all().select_related('cat'),
#         'cat_selected': 0,
#     }

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related('cat')
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

class WomenHome(ListView):
    #model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related('cat')



def page_not_found(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
def show_post(request,post_slug):
    post = get_object_or_404(Women,slug=post_slug)
    data = {'title': post.title,
            'menu': menu,
            'post': post,
            'cat_selected': 1,
            }
    #return HttpResponse(f"Отображение статьи с id = {post_id}")
    return render(request,'women/post.html',context=data)

class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST,request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form':form
#
#     }
#     return render(request,'women/addpage.html',data)
#
# class AddPage(View):
#     def get(self,request):
#         form = AddPostForm()
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)
#
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         data = {
#             'menu': menu,
#             'title': 'Добавление статьи',
#             'form': form
#         }
#         return render(request, 'women/addpage.html', data)

# class AddPage(FormView):
#     form_class = AddPostForm
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class AddPage(CreateView):
    form_class = AddPostForm
    #model = Women
    #fields = '__all__'
    template_name = 'women/addpage.html'
    #success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Добавление статьи',
    }

class UpdatePage(UpdateView):
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Редактирование статьи',
    }


def contact(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")
# def handle_uploaded_file(f):
#     with open(f"uploads/{f.name}", "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()

        #        handle_uploaded_file(request.FILES['file_upload'])
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})

def show_category(request,cat_slug):
    category=get_object_or_404(Category,slug=cat_slug)
    posts= Women.published.filter(cat_id=category.pk).select_related('cat')
    data = {'title': f'Рубрика: {category.name}',
            'menu': menu,
            'posts': posts,
            'cat_selected':category.pk,
            }
    return render(request, 'women/index.html', context=data)

class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

# def show_tag_postlist(request,tag_slug):
#     tag=get_object_or_404(TagPost,slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')
#
#     data = {'title': f'Тег: {tag.tag}',
#             'menu': menu,
#             'posts': posts,
#             'cat_selected': None,
#             }
#
#     return render(request, 'women/index.html', context=data)

class TagPostList(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')



#
#
# def categories (request,cat_id):
#     return HttpResponse(f"<h1>Статьи к категориям</h1><p>id: {cat_id}</p>")
#
# def categories_by_slug(request,cat_slug):
#     return HttpResponse(f"<h1>Статьи к категориям</h1><p>slug: {cat_slug}</p>")
#



# def archive(request,year):
#
#     if year >2023:
#         uri = reverse('cats',args=('music',))
#         #return redirect(uri)
#         #return HttpResponsePermanentRedirect(uri)
#         #return HttpResponseRedirect(uri)
#         return redirect(index)
#     return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")
#     # if year != 2023 and year != 1990:
#     #     raise Http404()
#     # else:
#     #     return HttpResponse(f"posts: {year}")
#
#
#
# def post_detail(request):
#     if request.GET:
#         keys = request.GET.dict()
#         l = []
#         for element in keys.items():
#             j = f"{element[0]}={element[1]}"
#             l.append(j)
#         h = "|".join(l)
#
#         return HttpResponse(h)
#     return HttpResponse("GET is empty")

# return HttpResponse(f"{request.GET}={request.GET.values()}|")

