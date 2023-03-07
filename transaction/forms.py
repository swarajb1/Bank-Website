from django import forms
from django.core.exceptions import ValidationError

from account.models import Account
from account.forms import valid_account_id_format
from transaction.models import Transaction



class TransactionForm (forms.Form):
    account_id          = forms.CharField(label='Beneficiary Account ID', min_length=5, max_length=5, required=True, widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    time_code           = forms.IntegerField(label="Time Code", required=True)
    transaction_coins   = forms.IntegerField(label="Transaction Coins", required=True)
    remarks             = forms.CharField(label="Remarks", max_length=100, required=False)


    def clean_account_id(self):
        account_id = self.cleaned_data['account_id'].upper()

        if not valid_account_id_format(account_id):
            raise  ValidationError("Account ID does not satisfy valid format: <alphabet><alphabet><digit><digit><digit>.")

        r = Account.objects.filter(account_id=account_id)
        if not r.count() : # because account_id is unique, r.count() can only be 0 or 1
            raise  ValidationError("Account ID does not exist.")

        return account_id
    
    def clean_transaction_coins(self):
        transaction_coins = self.cleaned_data['transaction_coins']

        if transaction_coins <= 0:
            raise  ValidationError("Number of Coins to be transferred cannot be '0' or negative.")

        if transaction_coins > 100000:
            raise  ValidationError("Number of Coins to be transferred cannot be greater than 100,000 Coins.")

        return transaction_coins


    def save(self, sender_id, commit=True):
        transaction = Transaction.objects.create_transaction(
            sender_id=sender_id, 
            receiver_id=self.cleaned_data['account_id'], 
            transaction_coins=self.cleaned_data['transaction_coins'], 
            remarks=self.cleaned_data['remarks']
            )

        return transaction



