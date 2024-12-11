from django.db import models

# Modelo para Conta Bancária
class Account(models.Model):
    account_number = models.CharField(max_length=20, unique=True)  # Número único da conta
    owner_name = models.CharField(max_length=100)  # Nome do titular
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Saldo inicial
    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação

    def __str__(self):
        return f"{self.account_number} - {self.owner_name}"

    def depositar(self, valor):
        """Método para depositar dinheiro na conta"""
        if valor > 0:
            self.balance += valor
            self.save()
            # Criando a transação de depósito
            Transaction.objects.create(account=self, transaction_type='Deposit', amount=valor)
            return True
        return False

    def sacar(self, valor):
        """Método para sacar dinheiro da conta"""
        if valor > 0 and self.balance >= valor:
            self.balance -= valor
            self.save()
            # Criando a transação de saque
            Transaction.objects.create(account=self, transaction_type='Withdraw', amount=valor)
            return True
        return False

# Modelo para Transações
class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)  # Conta vinculada
    transaction_type = models.CharField(max_length=10, choices=[('Deposit', 'Depósito'), ('Withdraw', 'Saque')])  # Tipo de transação
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da transação
    timestamp = models.DateTimeField(auto_now_add=True)  # Data e hora da transação

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.timestamp})"
