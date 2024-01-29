from django.shortcuts import render, redirect
from account.models import KYC, Account
from account.forms import KYCForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.forms import CreditCardForm
from core.models import CreditCard, Transaction, Notification


@login_required
def account(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, f'You have not submitted your KYC details!')
            return redirect('account:kyc-reg')
        account = Account.objects.get(user=request.user)
    else:
        messages.warning(request, f'You are not logged in!')
        return redirect('userauths:sign-in')
    context = {"kyc": kyc, 'account': account}
    return render(request, 'account/account.html', context)


@login_required
def kyc_registration(request):
    user = request.user
    account = Account.objects.get(user=request.user)

    try:
        kyc = KYC.objects.get(user=user)
    except:
        kyc = None

    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = user
            new_form.account = account
            new_form.save()
            messages.success(request, f'KYC details saved successfully!')
            return redirect('core:index')
    else:
        form = KYCForm(instance=kyc)

    context = {
        'form': form,
        "account": account,
        "kyc": kyc,
    }

    return render(request, "account/kyc-form.html", context)


def dashboard(request):
    if request.user.is_authenticated:
        try:
            kyc = KYC.objects.get(user=request.user)
        except:
            messages.warning(request, f'You have not submitted your KYC details!')
            return redirect('account:kyc-reg')
        recent_transfer = Transaction.objects.filter(sender=request.user, transaction_type="transfer", status="completed").order_by("-id")[:1]
        recent_received_transfer = Transaction.objects.filter(receiver=request.user, transaction_type="transfer").order_by('-id')[:1]
        sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by('-id')
        receiver_transaction = Transaction.objects.filter(receiver=request.user, transaction_type="transfer").order_by('-id')
        request_sender_transaction = Transaction.objects.filter(sender=request.user, transaction_type="request")
        request_receiver_transaction = Transaction.objects.filter(receiver=request.user, transaction_type="request")
        account = Account.objects.get(user=request.user)
        credit_card = CreditCard.objects.filter(user=request.user).order_by('-id')
        if request.method == "POST":
            form = CreditCardForm(request.POST)
            if form.is_valid():
                new_form = form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                Notification.objects.create(
                    user=request.user,
                    notification_type="Added Credit Card"
                )
                card_id = new_form.card_id
                messages.success(request, 'Card Added Successfully!')
                return redirect('account:dashboard')
        else:
            form = CreditCardForm()
    else:
        messages.warning(request, f'You are not logged in!')
        return redirect('userauths:sign-in')
    context = {"kyc": kyc,
               'account': account,
               'form': form,
               'credit_card': credit_card,
               "sender_transaction": sender_transaction,
               "receiver_transaction": receiver_transaction,
               "request_sender_transaction": request_sender_transaction,
               "request_receiver_transaction": request_receiver_transaction,
               "recent_transfer": recent_transfer,
               'recent_received_transfer': recent_received_transfer}
    return render(request, 'account/dashboard.html', context)






