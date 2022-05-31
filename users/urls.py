from django.contrib import admin
from django.contrib.auth import views as authview
from django.urls import path
from . import views

#namespace
app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', authview.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', authview.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('profile/',views.profile, name='profile'),
    path('createprofile/',views.create_profile, name='createprofile'),
    path('sellerprofile/<int:id>/', views.seller_profile, name='sellerprofile'),
]