from .models import Account
import logging
from django.utils import timezone
from transaction.models import Transaction

class MyAuthBackend(object):
    def authenticate(self, account_id, password):    
        try:
            account = Account.objects.get(account_id=account_id)
            if account.check_password(password):
                account.last_login = timezone.now()
                return account
            else:
                return None
        except Account.DoesNotExist:
            logging.getLogger("error_logger").error(f"Account with Account ID: {account_id} does not exist")
            return None
        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None


    def get_user(self, account_id):
        try:
            account = Account.objects.get(account_id=account_id)
            if account.is_active:
                return account
            return None
        except Account.DoesNotExist:
            logging.getLogger("error_logger").error(f"Account with Account ID: {account_id} not found")
            return None




def create_banks_account():
    # AA, OO and NU are created as superusers and the rest 673 account are admin accounts
    ls = ["AA000", "OO000", "NU000"]
    for acc in ls:
        Account.objects.create_superuser(
            account_id=acc, 
            identification="BANK " + acc[:2],
            password="landscape"
        ) 
        Transaction.objects.create_transaction(
            sender_id="NU000", 
            receiver_id=acc, 
            transaction_coins=0, 
            remarks="New Account Creation"
        )

    # ------------------------------
    path_File = "E:\\aa exp\\websiteProject\\gcbse\\bank_ids.txt"
    with open(path_File, 'r') as idFile:
        list1 = idFile.read()

    list2 = list1.split("\n")

    for acc in list2:
        Account.objects.create_adminuser(
            account_id=acc, 
            identification="BANK " + acc[:2],
            password="landscape"
        )    
        
        Transaction.objects.create_transaction(
            sender_id="NU000", 
            receiver_id=acc, 
            transaction_coins=0, 
            remarks="New Account Creation"
        )    
        
    return



