from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'owner_name', 'balance', 'created_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')