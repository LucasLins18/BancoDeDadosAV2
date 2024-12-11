from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Account, Transaction
from .forms import DepositForm, WithdrawForm

# View para Criar Conta
def create_account(request):
    if request.method == 'POST':
        account_number = request.POST['account_number']
        owner_name = request.POST['owner_name']
        initial_balance = float(request.POST['balance'])

        # Verifica se o número da conta é único
        if Account.objects.filter(account_number=account_number).exists():
            messages.error(request, 'Número de conta já existe!')
            return redirect('create_account')

        # Cria a conta
        Account.objects.create(account_number=account_number, owner_name=owner_name, balance=initial_balance)
        messages.success(request, 'Conta criada com sucesso!')
        return redirect('create_account')

    return render(request, 'accounts/create_account.html')


# View para Depósito
def deposit(request):
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            amount = form.cleaned_data['amount']
            
            try:
                account = Account.objects.get(account_number=account_number)  # Buscar a conta
                if amount <= 0:
                    messages.error(request, "O valor do depósito deve ser positivo.")
                else:
                    # Realiza o depósito
                    account.balance += amount
                    account.save()
                    
                    # Registrar a transação
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Deposit',
                        amount=amount
                    )
                    messages.success(request, f"Depósito de R$ {amount} realizado com sucesso!")
            except Account.DoesNotExist:
                messages.error(request, "Conta não encontrada.")

            return redirect('deposit')
    else:
        form = DepositForm()

    return render(request, 'accounts/deposit.html', {'form': form})


# View para Saque
def withdraw(request):
    if request.method == "POST":
        form = WithdrawForm(request.POST)
        if form.is_valid():
            account_number = form.cleaned_data['account_number']
            amount = form.cleaned_data['amount']
            
            try:
                account = Account.objects.get(account_number=account_number)  # Buscar a conta
                if amount <= 0:
                    messages.error(request, "O valor do saque deve ser positivo.")
                elif account.balance >= amount:
                    # Realiza o saque
                    account.balance -= amount
                    account.save()

                    # Registrar a transação
                    Transaction.objects.create(
                        account=account,
                        transaction_type='Withdraw',
                        amount=amount
                    )
                    messages.success(request, f"Saque de R$ {amount} realizado com sucesso!")
                else:
                    messages.error(request, "Saldo insuficiente para realizar o saque.")
            except Account.DoesNotExist:
                messages.error(request, "Conta não encontrada.")

            return redirect('withdraw')
    else:
        form = WithdrawForm()

    return render(request, 'accounts/withdraw.html', {'form': form})

# View para Consultar Saldo
def check_balance(request):
    if request.method == "POST":
        account_number = request.POST['account_number']
        
        try:
            # Buscar a conta com o número informado
            account = Account.objects.get(account_number=account_number)
            messages.success(request, f"O saldo da conta {account_number} é R$ {account.balance}")
        except Account.DoesNotExist:
            messages.error(request, "Conta não encontrada. Verifique o número da conta e tente novamente.")
        
        return redirect('check_balance')  # Redireciona de volta para a página de consulta de saldo
    
    return render(request, 'accounts/check_balance.html')
    
# View para Encerrar Conta
def close_account(request):
    if request.method == "POST":
        account_number = request.POST['account_number']
        
        try:
            # Tenta buscar a conta com o número fornecido
            account = Account.objects.get(account_number=account_number)
            account.delete()  # Exclui a conta do banco de dados
            messages.success(request, f"Conta {account_number} encerrada com sucesso!")
        except Account.DoesNotExist:
            messages.error(request, f"Conta {account_number} não encontrada!")
        
        return redirect('close_account')  # Redireciona para a mesma página (ou para onde você desejar)
    
    return render(request, 'accounts/close_account.html')

# View para exibir o saldo (formulário GET)
def balance(request):
    account_number = request.GET.get('account_number')
    try:
        account = Account.objects.get(account_number=account_number)
        return render(request, 'accounts/balance.html', {'account': account})
    except Account.DoesNotExist:
        return render(request, 'accounts/balance.html', {'error': 'Conta não encontrada.'})

# View para Exibir Histórico de Transações
def transaction_history(request):
    if request.method == "POST":
        account_number = request.POST['account_number']
        
        try:
            account = Account.objects.get(account_number=account_number)
            transactions = Transaction.objects.filter(account=account).order_by('-timestamp')  # Ordena as transações por data
            
            return render(request, 'accounts/transaction_history.html', {'account': account, 'transactions': transactions})
        except Account.DoesNotExist:
            messages.error(request, "Conta não encontrada. Verifique o número da conta e tente novamente.")
            return redirect('transaction_history')
    
    return render(request, 'accounts/transaction_history.html')
