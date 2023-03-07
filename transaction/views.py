from django.shortcuts import render, redirect
from django.contrib import messages
from random import randint
import pytz
from datetime import datetime
from gcbse import settings

from transaction.forms import TransactionForm
from .backend import (
    check_transaction, 
    history_context, 
    coins_in_circulation, 
    number_to_international_format, 
    transaction_charges_payment,
    trail_transaction
    )


def coins_transfer_view (request):
    context = {}

    if request.user.is_authenticated:
        # only when user is authenticated, transaction page is loaded otherwise redirect to index
        acc_coins = number_to_international_format(request.user.coins)


        if "000" in request.user.account_id:
            tr_charges = "--"
        else:
            tr_charges = number_to_international_format(request.user.transaction_charges) + " Coins"

        class_names = ["other_account", "transaction_charges", "annual_charges"]

        all_list = [
            [
                ["other_account", "transaction_charges", "annual_charges"],
                [
                    ["Account ID", request.user.account_id],
                    ["Account Name", request.user.account_name],
                    ["Coins Balance", acc_coins + " Coins"],
                ]
            ],
            [
                ["transaction_charges"],
                [
                    ["Current Transaction Charges", tr_charges],
                ]
            ],
            [
                ["annual_charges"],
                [
                    ["Current Annual Charges", "---"],
                ]
            ],
        ]

        for class_name in class_names:
            context[class_name] = []
            for item in all_list:
                if class_name in item[0]:
                    for row in item[1]:
                        context[class_name].append(row)

        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Coins Transfer Page"


        if request.method == 'POST':
            form = TransactionForm(data=request.POST)
            if form.is_valid():
                beneficiary_account_id = form.cleaned_data.get('account_id')
                transaction_coins = form.cleaned_data.get('transaction_coins')
                time_code = form.cleaned_data.get('time_code')
                user_account_id = request.user.account_id
                check_t = check_transaction(
                    user_account_id=user_account_id, beneficiary_account_id=beneficiary_account_id, 
                    time_code=time_code,
                    transaction_coins=transaction_coins)
                if check_t[0]:
                    form.save(sender_id=user_account_id)
                    messages.info(request, "Transanction completed SUCCESSFULLY.")
                    return redirect('transaction:transaction_history')
                else:
                    messages.error(request, check_t[1])
                    messages.info(request, "Transanction is NOT completed.")
                    return redirect('transaction:coins_transfer')
            else:
                messages.info(request, "Transanction is NOT completed.")
                context['transaction_form'] = form
        else: # GET request
            form = TransactionForm()
            context['transaction_form'] = form
        return render(request, 'account/coins_transfer.html', context)
    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')









def transaction_view (request):
    context = {}

    if request.user.is_authenticated:
        # only when user is authenticated, transaction page is loaded otherwise redirect to index
        acc_coins = number_to_international_format(request.user.coins)
        context['account_info'] = [
            ["Account ID", request.user.account_id],
            ["Account Name", request.user.account_name],
            ["Coins Balance", acc_coins + " Coins"],
        ]

        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Transfer to Other Accounts"

        if request.method == 'POST':
            form = TransactionForm(data=request.POST)
            if form.is_valid():
                beneficiary_account_id = form.cleaned_data.get('account_id')
                transaction_coins = form.cleaned_data.get('transaction_coins')
                time_code = form.cleaned_data.get('time_code')
                user_account_id = request.user.account_id
                check_t = check_transaction(
                    user_account_id=user_account_id, beneficiary_account_id=beneficiary_account_id, 
                    time_code=time_code,
                    transaction_coins=transaction_coins)
                if check_t[0]:
                    form.save(sender_id=user_account_id)
                    messages.info(request, "Transanction completed SUCCESSFULLY.")
                    return redirect('transaction:transaction_history')
                else:
                    messages.error(request, check_t[1])
                    messages.info(request, "Transanction is NOT completed.")
                    return redirect('transaction:transaction')
            else:
                messages.info(request, "Transanction is NOT completed.")
                context['transaction_form'] = form
        else: # GET request
            form = TransactionForm()
            context['transaction_form'] = form
        return render(request, 'account/transaction.html', context)
    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')


def transaction_history_view (request):
    context = {}
    if request.user.is_authenticated:
        user_account_id = request.user.account_id

        ls = history_context(user_account_id)
        context['transaction_headers'] = ls.pop(0)

        context['list_of_pages'] = []

        num_pages = len(ls)//20
        if len(ls)%20 != 0:
            num_pages += 1

        count = 0
        for _ in range(num_pages):
            list2 = []
            for i in range(20):
                list2.append(ls[count])
                count += 1
                if count == len(ls):
                    break

            context['list_of_pages'].append(list2)

        ls_pages = []
        if num_pages > 1:
            for i in range(num_pages):
                ls_pages.append(i+1)
        context['pages_num'] = ls_pages


        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Transaction History"

        return render(request, 'transaction/history.html', context)
    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')



def coins_circulation_view (request):
    context = {}

    IND = pytz.timezone(settings.TIME_ZONE) 
    context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
    context['page_name'] = "Coins in Circulation"

    if request.user.is_authenticated:
        context['coins_circulation'] = ["Coins in Circulation", coins_in_circulation()]
        return render(request, 'account/dashboard.html', context)

    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')


def transaction_charges_view (request):
    # LATER make sure that when transaction charges reach 1 million then account is set to inactive till charges are paid
    context = {}

    if request.user.is_authenticated:
        # only when user is authenticated, transaction page is loaded otherwise redirect to index        
        transaction_coins = request.user.transaction_charges

        acc_coins = number_to_international_format(request.user.coins)
        if "000" in request.user.account_id:
            tr_charges = "--"
        else:
            tr_charges = number_to_international_format(transaction_coins) + " Coins"

        context['account_info'] = [
            ["Account ID", request.user.account_id],
            ["Account Name", request.user.account_name],
            ["Coins Balance", acc_coins + " Coins"],
            ["Transaction Charges", tr_charges],
        ]

        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Transfer for Transaction Charges"

        context['btn_disabled'] = (transaction_coins == 0)

        if not context['btn_disabled']:
            context['more_message'] = "Pay " + context['account_info'][3][1] + " as Transaction Charges"
        else:
            if "000" in context['account_info'][0][1]:
                context['more_message'] = "Accounts of Bank itself are NOT CHARGED."
            else:
                context['more_message'] = "You currently have no transaction charges."

        if request.method == 'POST':
            bank_account_id = "AA000"
            user_account_id = request.user.account_id
            check_t = check_transaction(
                user_account_id=user_account_id, beneficiary_account_id=bank_account_id, transaction_coins=transaction_coins)
            if check_t[0]:
                transaction_charges_payment(user_account_id)
                messages.info(request, "Transanction completed SUCCESSFULLY.")
                return redirect('transaction:transaction_history')
            else:
                messages.error(request, check_t[1])
                return redirect('transaction:transaction_charges')
        else: # GET request
            return render(request, 'account/transaction.html', context)
    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')


def annual_charges_view (request):
    context = {}

    if request.user.is_authenticated:
        # only when user is authenticated, transaction page is loaded otherwise redirect to index
        transaction_coins = 0
        
        acc_coins = number_to_international_format(request.user.coins)
        context['account_info'] = [
            ["Account ID", request.user.account_id],
            ["Account Name", request.user.account_name],
            ["Coins Balance", acc_coins + " Coins"],
            ["Annual Charges", "--"],
        ]

        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Transfer for Annnual Charges"

        context['btn_disabled'] = (transaction_coins == 0)

        if not context['btn_disabled']:
            context['more_message'] = "Pay " + str(transaction_coins) + " as Transaction Charges"
        else:
            if "000" in context['account_info'][0][1]:
                context['more_message'] = "Accounts of Bank itself are NOT CHARGED."
            else:
                context['more_message'] = "You currently have no transaction charges."

        if request.method == 'POST':
            bank_account_id = "AA000"
            user_account_id = request.user.account_id
            check_t = check_transaction(
                user_account_id=user_account_id, beneficiary_account_id=bank_account_id, transaction_coins=transaction_coins)
            if check_t[0]:
                transaction_charges_payment(user_account_id)
                messages.info(request, "Transanction completed SUCCESSFULLY.")
                return redirect('transaction:transaction_history')
            else:
                messages.error(request, check_t[1])
                return redirect('transaction:annual_charges')
        else: # GET request
            return render(request, 'account/transaction.html', context)
    else: # if user is not already authenticated so redirect to index
        return redirect('public:index')



def trail_transactions_view(request):
    context = {}

    for _ in range(10):
        if randint(1, 3) == 1:
            sender_id = "BB000"
            receiver_id = "CC000"
        else:
            sender_id = "CC000"
            receiver_id = "BB000"

        coins = randint(1000,2000)

        trail_transaction(sender_id, receiver_id, coins)
    
    return redirect('transaction:transaction_history')



