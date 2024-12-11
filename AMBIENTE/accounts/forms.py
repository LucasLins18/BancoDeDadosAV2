from django import forms

class DepositForm(forms.Form):
    account_number = forms.CharField(max_length=20, label="Número da Conta")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Valor a Depositar", min_value=0.01)

class WithdrawForm(forms.Form):
    account_number = forms.CharField(max_length=20, label="Número da Conta")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="Valor a Sacar", min_value=0.01)
