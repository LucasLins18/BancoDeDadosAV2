# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Definindo a URL para criação de conta
    path('create/', views.create_account, name='create_account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('balance/', views.check_balance, name='check_balance'), 
    path('close/', views.close_account, name='close_account'),
    path('transactions/', views.transaction_history, name='transaction_history'),  # URL para o histórico de transações
]