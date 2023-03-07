from django import forms
from django.contrib.auth.forms import  UserCreationForm, AuthenticationForm

from transaction.models import Transaction
from account.models import Account
from django.core.exceptions import ValidationError


class RegistrationForm (UserCreationForm):
    account_id      = (
        forms.CharField(
            label="Account ID", 
            min_length=5, 
            max_length=5, 
            required=True, 
            widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'})
        )
    )
    
    account_name    = forms.CharField(label='Account Name', required=True, max_length=100, widget=forms.TextInput)
    
    identification  = forms.CharField(label="Identification", min_length=4, max_length=150, required=True, widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    
    email = forms.EmailField(label='Email', required=False, max_length=50, widget=forms.TextInput(attrs={'style': 'text-transform:lowercase;'}))

    password1       = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)
    password2       = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = Account
        fields = ("account_id", "account_name", "identification", "email", "password1", "password2")

    def clean_account_id(self):
        account_id = self.cleaned_data['account_id'].upper()
        r = Account.objects.filter(account_id=account_id)
        if r.count():
            raise  ValidationError("Account ID already exists.")

        if not valid_account_id_format(account_id):
            raise  ValidationError("Account ID does not satisfy valid format: <alphabet><alphabet><digit><digit><digit>.")

        return account_id

    def clean_account_name(self):
        account_name = self.cleaned_data['account_name'].title()
        r = Account.objects.filter(account_name=account_name)
        if r.count():
            raise  ValidationError("Account Name already exists.")
        return account_name

    def clean_identification(self):
        identification = self.cleaned_data['identification'].upper()
        r = Account.objects.filter(identification=identification)
        if r.count():
            raise  ValidationError("Identification already exists.")
        return identification

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = Account.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        
        return password2

    def save(self, sender_id, commit=True):
        account = Account.objects.create_user(
            account_id=self.cleaned_data['account_id'], 
            account_name=self.cleaned_data['account_name'],
            email=self.cleaned_data['email'],
            identification=self.cleaned_data['identification'],
            password=self.cleaned_data['password1']
        )

        transaction = Transaction.objects.create_transaction(
            sender_id=sender_id, 
            receiver_id=self.cleaned_data['account_id'], 
            transaction_coins=0, 
            remarks=f"New Account Creation by {sender_id}"
        )

        return account




class LoginForm (AuthenticationForm):
    username = forms.CharField(label='Account ID', min_length=5, max_length=5, required=True, widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=True)

    class Meta:
        model = Account
        fields = ("account_id", "password")

    def clean_username(self):
        account_id = self.cleaned_data['username'].upper()
        r = Account.objects.filter(account_id=account_id)
        if not r.count(): # Error when r.count is 0 
            raise  ValidationError("Account ID does NOT exists.")

        if not valid_account_id_format(account_id):
            raise  ValidationError("Account ID does not satisfy valid format: <alphabet><alphabet><digit><digit><digit>.")

        return account_id


    def clean_password(self):
        password = self.cleaned_data.get('password')

        return password



def valid_account_id_format(z):
    if len(z) != 5:
        return False
    if (ord(z[0]) not in range(65, 92) or # Capital alphabet
        ord(z[1]) not in range(65, 92) or # Capital alphabet
        ord(z[2]) not in range(48, 58) or # Digit 
        ord(z[3]) not in range(48, 58) or # Digit
        ord(z[4]) not in range(48, 58)):  # Digit
        return False
    return True


