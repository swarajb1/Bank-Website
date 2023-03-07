from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, LoginForm
import pytz
from datetime import datetime
from gcbse import settings
from account.models import Account
from transaction.backend import number_to_international_format, last_transaction


# ---------------------------------- start of REGISTER, LOGIN and LOGOUT

def registration_view (request):
    context = {}
    if request.user.is_authenticated and request.user.is_admin:
    # only when user is authenticated and is admin only then is register page loaded otherwise redirect to public:index 
        IND = pytz.timezone(settings.TIME_ZONE) 
        context['datetime'] = datetime.now(tz=IND).strftime("%A, %d %b %Y %H:%M:%S %Z")
        context['page_name'] = "Register New User"


        if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            if form.is_valid():
                form.save(sender_id=request.user.account_id)
                account_id = form.cleaned_data.get('account_id')
                messages.success(request, f"{account_id} Account ID Successfully REGISTERED.")
                return redirect('transaction:transaction_history')
            else:
                context['registration_form'] = form
        else: # GET request
            form = RegistrationForm()
            context['registration_form'] = form
        # return render(request, 'account/login_register.html', context)
        return render(request, 'account/register.html', context)
    else: # user is already authenticated so redirect to dashboard
        return redirect('public:index')

    # -----------------------------------------
    # When registration is not done by ADMIN by then users themselves

    # if not request.user.is_authenticated:
    # # only when user is not authenticated, register page is loaded otherwise redirect to dashboard 
    #     if request.method == 'POST':
    #         form = RegistrationForm(data=request.POST)
    #         if form.is_valid():
    #             form.save()
    #             account_id = form.cleaned_data.get('account_id')
    #             raw_password = form.cleaned_data.get('password1')
    #             account = authenticate(account_id=account_id, password=raw_password)
    #             login(request, account)
    #             messages.success(request, f"{account_id} Successfully REGISTERED.")
    #             return redirect('account:dashboard')
    #         else:
    #             context['registration_form'] = form
    #     else: # GET request
    #         form = RegistrationForm()
    #         context['registration_form'] = form
    #     return render(request, 'account/login_register.html', context)
    # else: # user is already authenticated so redirect to dashboard
    #     return redirect('public:index')


def logout_view (request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully Logged Out.")
    return redirect('public:index')


def login_view (request):
    context = {}

    if not request.user.is_authenticated:
        # only when user is not authenticated, login page is loaded otherwise redirect to dashboard 
        if request.method == 'POST':
            form = LoginForm(data=request.POST)
            if form.is_valid():
                account_id = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                account = authenticate(account_id=account_id, password=password)
                if account is not None:
                    login(request, account)
                    messages.info(request, "Successfully Logged In.")
                    return redirect('account:account')
                    # return redirect('account:dashboard')
                else:
                    messages.error(request, "Incorrect Credentials, Please try again.")
                    return redirect('public:index')
            else:
                messages.error(request, "Invalid Credentials, Please try again.")
                context['login_form'] = form
        else: # GET request
            form = LoginForm()
            context['login_form'] = form
        return render(request, 'account/login_register.html', context)
    else: # user is already authenticated so redirect to dashboard
        return redirect('public:index')


# ---------------------------------- end of REGISTER, LOGIN and LOGOUT


def account_view (request):
    context = {}

    if request.user.is_authenticated:
        # only when user is authenticated to account 
        acc_coins = number_to_international_format(request.user.coins)
        last_login_time = request.user.last_login.astimezone(pytz.timezone('Asia/Calcutta')).strftime("%d %B %Y %H:%M %Z")
        # last_transaction_time = last_transaction(request.user.account_id).astimezone(pytz.timezone('Asia/Calcutta')).strftime("%d %B %Y %H:%M %Z")
        last_transaction_time = 0

        if "000" in request.user.account_id:
            tr_charges = "--"
        else:
            tr_charges = number_to_international_format(request.user.transaction_charges) + " Coins"

        class_names = ["dashboard", "account_summary", "account_details", "my_profile"]

        all_list = [
            [
                ["dashboard", "account_summary", "account_details", "my_profile"],
                [
                    ["Account ID", request.user.account_id],
                    ["Account Name", request.user.account_name],
                ]
            ],
            [
                ["my_profile"],
                [
                    ["Identification", request.user.identification],
                    ["Email", request.user.email],
                ]
            ],
            [
                ["dashboard", "account_summary"],
                [
                    ["Coins Balance", acc_coins + " Coins"],
                    ["Current Transaction Charges", tr_charges],
                    ["Current Annual Charges", "---"],
                ]
            ],
            [
                ["account_summary", "account_details"],
                [
                    ["Last Transaction Time", last_transaction_time],
                    ["Account Last Login", last_login_time],
                ]
            ],
            [
                ["account_details", "my_profile"],
                [
                    ["Account Opening Date", request.user.date_joined.strftime("%d %B %Y")],
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
        context['page_name'] = "Account Dashboard"

        return render(request, 'account/account.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')




def site_map_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sitemap.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')





# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------
def sorry_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')


def change_password_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')



def session_summary_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')



def deposits_view (request):
    context = {}
    # like fixed deposits which can only withdrawn after maturity date/ also retirement funds
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')



def services_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')



def beneficiary_add_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')



def beneficiary_view_view (request):
    context = {}
    if request.user.is_authenticated:
        # only when user is authenticated, login page is loaded otherwise redirect to dashboard 
        return render(request, 'account/sorry.html', context)
    else: # user is not authenticated so redirect to index
        return redirect('public:index')


# ------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------



from transaction.models import Transaction

def initialise_view(request):
    context = {}
    l = []
    r = Transaction.objects.all()
    prev = ""
    count = 0
    # for transaction in r:
    #     if prev == transaction.transaction_id[:15]:
    #         count += 1
    #     else:
    #         prev = transaction.transaction_id[:15]
    #         l.append(count)
    #         count = 1
    for transaction in r:
        if prev == transaction.transaction_time.replace(microsecond=0).strftime("%Y%m%d-%H%M%S"):
            count += 1
        else:
            prev = transaction.transaction_time.replace(microsecond=0).strftime("%Y%m%d-%H%M%S")
            l.append(count)
            count = 1

    context['extra_info'] = l

    return render(request, 'account/sorry.html', context)


