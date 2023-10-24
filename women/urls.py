from django.contrib import admin
from django.urls import path, re_path, register_converter
from . import converters

#from women.views import index,categories
from . import views


register_converter(converters.FourDigitYearConverter,'year4')

urlpatterns = [
    #path('', views.index,name='home'),
    #path('', views.WomenHome.as_view(extra_context = {'title':'Главная страница сайта'}),name='home'),
    path('', views.WomenHome.as_view(),name='home'),
    path('about/', views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'),
    path('addpage/', views.AddPage.as_view(), name='add_page'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/',views.ShowPost.as_view(),name='post'),
    path('category/<slug:cat_slug>/',views.WomenCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit_page'),


    # path('cats/<int:cat_id>/',views.categories,name='cat_id'),# http://127.0.0.1:8000/cats/2/
    # path('cats/<slug:cat_slug>/',views.categories_by_slug,name='cats'),# http://127.0.0.1:8000/cats/ddsfsdf/
    # #re_path(r"^archive/(?P<year>[0-9]{4})/",views.archive)
    # path("archive/<year4:year>/",views.archive,name='archive'),
    # path("test/",views.post_detail)
]


