from decimal import Decimal
from django.contrib import messages

from django.shortcuts import render, redirect
from core.models import CreditCard, Notification
from account.models import Account


def all_cards(request):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.filter(user=request.user)

    context = {
        "account":account,
        "credit_card":credit_card,
    }
    return render(request, "credit_card/all-card.html", context)


def card_detail(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    context = {'account': account, 'credit_card': credit_card}
    return render(request, 'credit_card/card-detail.html', context)


def fund_credit_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    account = request.user.account
    if request.method == 'POST':
        amount = request.POST.get('funding_amount') # 25
        if Decimal(amount) <= account.account_balance:
            account.account_balance -= Decimal(amount) # 14,700.00 - 20
            account.save()
            credit_card.amount += Decimal(amount)
            credit_card.save()
            Notification.objects.create(
                amount=amount,
                user=request.user,
                notification_type='Funded Credit Card'
            )
            messages.success(request, 'Funding successfully!')
            return redirect('core:card-detail', card_id)
        else:
            messages.error(request, 'Insufficient funds')
        return redirect('core:card-detail', card_id)


def withdraw_fund(request, card_id):
    account = Account.objects.get(user=request.user)
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if credit_card.amount >= Decimal(amount):
            account.account_balance += Decimal(amount)
            account.save()
            credit_card.amount -= Decimal(amount)
            credit_card.save()
            Notification.objects.create(
                user=request.user,
                amount=amount,
                notification_type="Withdrew Credit Card Funds"
            )
            messages.success(request, 'Withdraw successfully!')
            return redirect('core:card-detail', card_id)
        else:
            messages.error(request, 'Insufficient funds')
            return redirect('core:card-detail', card_id)


def delete_card(request, card_id):
    credit_card = CreditCard.objects.get(card_id=card_id, user=request.user)
    # New Feature
    # Before deleting card, it'll be nice to transfer all the money from the card to the main account balance.
    account = request.user.account
    if credit_card.amount > 0:
        account.account_balance += credit_card.amount
        account.save()
        Notification.objects.create(
            user=request.user,
            notification_type="Deleted Credit Card"
        )
    credit_card.delete()
    messages.success(request, 'Card deleted successfully!.')
    Notification.objects.create(
        user=request.user,
        notification_type="Deleted Credit Card"
    )
    return redirect('account:dashboard')







