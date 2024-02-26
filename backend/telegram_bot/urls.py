from django.contrib import admin
from django.urls import path, re_path
import telegram_bot.views as views
from rest_framework import routers


urlpatterns = [
    path('transactions/<pk>/', views.TransactionUpdateView.as_view()),
    path('transactions/', views.TransactionCreate.as_view()),
    path('bank-accounts/', views.BankAccountRetrieveView.as_view()),
    path('telegram-user/', views.TelegramUserCreateView.as_view()),
    path('package/', views.PackageView.as_view()),
    path('package/<pk>/', views.PackageView.as_view()),
]