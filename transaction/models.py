from django.db import models
from datetime import datetime
from dateutil import tz
from gcbse import settings


class TransactionManager (models.Manager):
    def create_transaction(self, sender_id, receiver_id, transaction_coins, remarks):
        IND = tz.gettz(settings.TIME_ZONE) 
        transaction_time = datetime.now(tz=IND)
        
        # # 'try' is used because when there is no transaction in dataase as for the very first transaction
        # try:
        #     r = Transaction.objects.latest('transaction_time')
        #     prev_id = r.transaction_id

        # except:
        #     prev_id = ""

        # t_datetime = transaction_time.strftime("%Y%m%d-%H%M%S")
        # transaction_id = queueSecond(prev_id, t_datetime)
        transaction_id = ""

        transaction = self.create(
            transaction_id=transaction_id,
            transaction_time=transaction_time,
            sender_id=sender_id,
            receiver_id=receiver_id,
            transaction_coins=transaction_coins,
            remarks=remarks,
            )
        return transaction




class Transaction (models.Model):
    transaction_id      = models.CharField(verbose_name="Transaction ID", max_length=21)
    # THINK LATER about max_length of transacion_id 
    transaction_time    = models.DateTimeField(verbose_name="Transaction Time", blank=False)
    sender_id           = models.CharField(verbose_name="Sender Account ID", max_length=5, blank=False)
    receiver_id         = models.CharField(verbose_name="Receiver Account ID", max_length=5, blank=False)
    transaction_coins   = models.PositiveIntegerField(verbose_name="Transaction Coins", default=0)
    remarks             = models.CharField(verbose_name="Remarks", max_length=100, blank=True)

    objects = TransactionManager()

    def __str__(self):
        return self.transaction_id






def queueSecond(prev_id, new_id_datetime):
    num = 0
    if prev_id:
        if prev_id[:15] == new_id_datetime:
            num = int(prev_id[-5:])+1   

    res = ""

    if num < 10:
        res = "0000" + str(num)
    elif num < 100:
        res = "000" + str(num)
    elif num < 1000:
        res = "00" + str(num)
    elif num < 10000:
        res = "0" + str(num)
    elif num < 100000:
        res = str(num)

    return new_id_datetime + "-" + res

