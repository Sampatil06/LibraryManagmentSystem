from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', views.register, name='register'),
    path('books/', views.books, name='books'),
    path('borrow/', views.borrow, name='borrow'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),


]
