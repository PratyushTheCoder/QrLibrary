from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register, name='register'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),
    path('qrcode_manage',views.qrcode_manage,name='qrcode_manage'),
    path('qrcode_create',views.qrcode_create,name='_create'),
    path('qrcode_search',views.qrcode_search,name='_search'),
]
