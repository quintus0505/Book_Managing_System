"""Book_managing_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.urls import path
from front import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('book_info/add_book/', views.add_book, name='add_book'),
    path('book_info/batch_book_in/', views.batch_book_in, name='batch_book_in'),
    path('book_info/batch_book_out/', views.batch_book_out, name='batch_book_out'),
    path('book_info/batch_import_book/', views.batch_import_book, name='batch_import_book'),
    path('user_info/batch_import_user/', views.batch_import_user, name='batch_import_user'),
    path('book_info/', views.book_info, name='book_info'),
    path('user_info/', views.user_info, name='user_info'),
    path('user_info/add_user/', views.add_user, name='add_user'),
    url(r'^alter_book_info/',views.alter_book_info),
    url(r'^alter_user_info/',views.alter_user_info),
    url(r'^borrow_book/',views.borrow_book),
]
