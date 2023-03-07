from account.models import Account
from .models import Transaction
from django.core.exceptions import ValidationError
import pytz


def check_transaction (user_account_id, beneficiary_account_id, time_code, transaction_coins):
    if transaction_coins == 0:
        return [False, "Transaction Coins cannot be '0'."]

    if user_account_id == beneficiary_account_id:
        return [False, "Beneficiary Account ID is the same as User Account ID."]

    beneficiary_account = Account.objects.get(account_id=beneficiary_account_id)
    beneficiary_account.coins += transaction_coins

    # checking whether the time code provided is the assigned time code for the benificiary account
    if time_code != beneficiary_account.time_code:
        return [False, f"Time Code provided does not match with the time code of Beneficiary Account {beneficiary_account_id}."]        

    # Account LIMITs
    if "000" not in beneficiary_account_id:
        # LIMIT on general accounts 1 million
        if beneficiary_account.coins > 1000000: # 1 Million coins = LIMIT
            return [False, "Beneficiary Account will exceed 'GENERAL account Coins LIMIT' after transaction, so Transaction cannot proceed."]

    else: 
        # LIMIT on bank's accounts is 2 billion
        if beneficiary_account.coins > 2000000000: # 2 Billion coins = LIMIT
            return [False, "Beneficiary Account will exceed 'BANK's account Coins LIMIT' after transaction, so Transaction cannot proceed."]


    user_account = Account.objects.get(account_id=user_account_id)
    user_account.coins -= transaction_coins
    if user_account.coins < 0:
        return [False, "User Account does not have enough coins."]

    if not ("000" in beneficiary_account_id or "000" in user_account_id):
        # transactions with the bank are not charged
        beneficiary_account.transaction_charges += 1
        user_account.transaction_charges += 1
    
    beneficiary_account.save()
    user_account.save()
    return [True, ""]



def history_context (user_account_id, number=100, date_from=0, date_to=0):

    r1 = Transaction.objects.filter(
            sender_id=user_account_id
            ).order_by('-transaction_time'
            )[:number]

    r2 = Transaction.objects.filter(
            receiver_id=user_account_id
            ).order_by('-transaction_time'
            )[:number]

    c1 = len(r1) # total number of transactions as sender
    c2 = len(r2) # total number of transactions as receiver

    headers = [
        "S.No.",
        "Transaction ID",
        "Transaction Time", 
        "Type", # "Type of Transaction",
        "Transaction with Account ID", 
        "Transaction Coins", 
        "Remarks", 
        "Balance"]

    context = []
    context.append(headers)
    balance = Account.objects.get(account_id=user_account_id).coins
    prev_trasanction_coins = 0
    
    count = 0
    i1, i2 = 0, 0
    totalcount = c1 + c2
    number = min(number, totalcount)

    for _ in range(number):
        count += 1
        ls = [count, "", "", "", "", "", "", ""]
        if i1 < c1 and i2 < c2: 
            if r1[i1].transaction_time > r2[i2].transaction_time:
                transaction = r1[i1]
                ls[3] = "Debit"
                i1 += 1
            else:
                transaction = r2[i2]
                ls[3] = "Credit"
                i2 += 1
        elif i1 == c1:
            transaction = r2[i2]
            ls[3] = "Credit"
            i2 += 1
        
        elif i2 == c2:
            transaction = r1[i1]
            ls[3] = "Debit"
            i1 += 1

        ls[1] = transaction.transaction_id 
        ls[2] = transaction.transaction_time.astimezone(pytz.timezone('Asia/Calcutta')).strftime("%d %B %Y %H:%M %Z")
        ls[5] = number_to_international_format(transaction.transaction_coins)
        ls[6] = transaction.remarks
        if ls[3] == "Debit":
            ls[4] = transaction.receiver_id
            balance += prev_trasanction_coins 
            prev_trasanction_coins = transaction.transaction_coins
        else: # ls[3] == "Credit"
            ls[4] = transaction.sender_id
            balance += prev_trasanction_coins
            prev_trasanction_coins = -1*transaction.transaction_coins

        ls[7] = number_to_international_format(balance)
        context.append(ls)

    # later check 'Limiting QuerySets' when the number of transactions to display exceed 15, then displaying only 15 and other in next page

    return context



def number_to_international_format(num):
    z = str(num)
    add = ""
    if z[0] == "-":
        z = z[1:]
        add= "-"
    
    z = z[::-1]

    res = ""
    for i in range(0,len(z)):
        if i%3 == 0 and not i == 0:
            res += ","
        res += z[i]
    
    res = add + res[::-1]
    return res



def coins_in_circulation ():
    coins_circulation = 0

    r = Account.objects.all()

    for account in r:
        coins_circulation += account.coins

    # Bank Zero account coins are not inside circulation
    r0 = Account.objects.get(account_id="OO000")
    coins_circulation -= r0.coins

    return number_to_international_format(coins_circulation) + " Coins"


def transaction_charges_payment(user_account_id, bank_account_id="AA000"):

    user_account = Account.objects.get(account_id=user_account_id)
    transaction_coins = user_account.transaction_charges
    user_account.transaction_charges = 0
    user_account.save()

    transaction = Transaction.objects.create_transaction(
        sender_id=user_account_id, 
        receiver_id=bank_account_id, 
        transaction_coins=transaction_coins, 
        remarks="Transaction Charges")

    return



def last_transaction (account_id):
    r1 = Transaction.objects.filter(sender_id=account_id).order_by('-transaction_time')
    r2 = Transaction.objects.filter(receiver_id=account_id).order_by('-transaction_time')


    if len(r1) > 0:
        if r1[0].transaction_time < r2[0].transaction_time:
            return r2[0].transaction_time
        else:
            return r1[0].transaction_time
    
    else: # the first transaction is the 'New Account Creation' as received always
        return r2[0].transaction_time

   

def trail_transaction (sender_id, receiver_id, transaction_coins):
    check = check_transaction(sender_id, receiver_id, 0, transaction_coins)
    if not check[0]:
        return
    Transaction.objects.create_transaction(
        sender_id=sender_id, 
        receiver_id=receiver_id, 
        transaction_coins=transaction_coins, 
        remarks="trail transactions"
        )
    return
    