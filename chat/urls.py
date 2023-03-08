from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('chats/', views.ChatSessionView.as_view()),
    path('chats/user', views.user.as_view()),
    path('chats/<uri>/', views.ChatSessionView.as_view()),
    path('chats/<uri>/messages/', views.ChatSessionMessageView.as_view()),
    path('chats/<uri>/seen/', views.seen.as_view()),
    path('chats/adminchat', views.adminchat.as_view()),
]