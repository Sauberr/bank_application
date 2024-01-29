from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from account.models import KYC, Account
from django.db.models import Q
from django.contrib import messages
from core.models import Transaction


@login_required()
def search_users_account_number(request):
    # account = Account.objects.filter(account_status='Active')
    account = Account.objects.all()
    query = request.POST.get('account_number')
    if query:
        account = account.filter(
            Q(account_number=query) |
            Q(account_id=query)
        ).distinct()

    context = {'account': account, 'query': query}
    return render(request, 'transfer/search-user-by-account-number.html', context)


def AmountTransfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning(request, f'Account does not exist!')
        return redirect('core:search-account')
    context = {'account': account}
    return render(request, 'transfer/amount-transfer.html', context)


def AmountTransferProcess(request, account_number):
    account = Account.objects.get(account_number=account_number) # get the account that the money would be sent to
    sender = request.user # get the person that is logged in
    receiver = account.user # get  the account of the person that is going to receive the money
    sender_account = request.user.account # get currently logged in users account that would send the money
    receiver_account = account # get the person account that would send the money
    if request.method == 'POST':
        amount = request.POST.get('amount-send')
        description = request.POST.get('description')

        if sender_account.account_balance >= Decimal(amount):
            new_transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                receiver=receiver,
                sender=sender,
                sender_account=sender_account,
                receiver_account=receiver_account,
                status="processing",
                transaction_type="transfer"
            )
            new_transaction.save()
            # Get the id of transaction that was created now
            transaction_id = new_transaction.transaction_id
            return redirect("core:transfer-confirmation", account.account_number, transaction_id)
        else:
            messages.warning(request, f'Insufficient funds!')
            return redirect('core:amount-transfer', account.account_number)
    else:
        messages.warning(request, f'Insufficient funds!')
        return redirect('account:account')


def TransferConfirmation(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, f'Transaction does not exist!')
        return redirect('account:account')
    context = {'account': account, 'transaction': transaction}
    return render(request, "transfer/transfer-confirmation.html", context)


def TransferProcess(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    sender = request.user
    receiver = account.user
    sender_account = request.user.account
    receiver_account = account
    completed = False
    if request.method == 'POST':
        pin_number = request.POST.get('pin-number')
        print(pin_number)
        if pin_number == sender_account.pin_number:
            transaction.status = 'completed'
            transaction.save()
            # Remove the amount that I am sending from my account balance and update my account
            sender_account.account_balance -= transaction.amount
            sender_account.save()
            # Add the amount that remove from my account to the person that I am sending the money
            account.account_balance += transaction.amount
            account.save()
            messages.success(request, 'Transfer Successful!')
            return redirect('core:transfer-completed', account.account_number, transaction.transaction_id)
        else:
            messages.warning(request, 'Incorrect Pin code.')
            return redirect('core:transfer-confirmation', account.account_number, transaction.transaction_id)
    else:
        messages.warning(request, 'An error occurred, Try again later.')
        return redirect('account:account')


def TransferCompleted(request, account_number, transaction_id):
    try:
        account = Account.objects.get(account_number=account_number)
        transaction = Transaction.objects.get(transaction_id=transaction_id)
    except:
        messages.warning(request, f'Transfer does not exist!')
        return redirect('account:account')
    context = {'account': account, 'transaction': transaction}
    return render(request, "transfer/transfer-completed.html", context)














