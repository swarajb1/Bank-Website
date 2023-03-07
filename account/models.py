from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator 


class AccountManager (BaseUserManager):
    def create_user(self, account_id, account_name, identification, email, password=None):
        if not account_id:
            raise ValueError("Account Holders must have an Account ID.")
        # if not identification:
        #     raise ValueError("Account Holders must have an Idendification Proof.")

        r = Account.objects.all()
        time_code = r.count() + 100000
        # adding 100,000 so that all code are of 6 digits

        user = (
            self.model(
                account_id = account_id,
                account_name = account_name,
                identification = identification,
                email = email,
                time_code = time_code,
                date_joined = datetime.datetime.now()
            )
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    


    # def create_superuser(self, account_id, account_name, identification, email, password):
    def create_superuser(self, account_id, password):
        user = (
            self.create_user(
                account_id=account_id.upper(),
                account_name = "account_name",
                identification = "identification",
                email = "email@email.com",
                password=password,
            )
        )
        # user = (
        #     self.create_user(
        #         account_id=account_id.upper(),
        #         # account_name = account_name,
        #         identification = identification,
        #         # email = email,
        #         password=password,
        #     )
        # )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


    def create_admin(self, account_id, identification, password):
        user = (
            self.create_user(
                account_id=account_id.upper(),
                # identification= identification,
                password=password,
            )
        )

        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, account_id, identification, password):
        # the staff will not have "000" accounts but regular accounts with some special permissions
        
        user = (
            self.create_user(
                account_id=account_id.upper(),
                identification= identification,
                password=password,
            )
        )

        user.is_staff = True
        user.save(using=self._db)
        return user




class Account (AbstractBaseUser):
    
    account_id          = models.CharField(verbose_name="Account ID", primary_key=True,max_length=5, unique=True, blank=False)
                                                                                        
    email               = models.EmailField(verbose_name="Email", max_length=50, blank=True)
    identification      = models.CharField(verbose_name="Identification Proof", max_length=150, blank=True)
    # identification      = models.CharField(verbose_name="Identification Proof", max_length=150, unique=True, blank=True)
    
    account_name        = models.CharField(verbose_name="Account Holder Name", max_length=100, blank=True)
    coins               = models.PositiveIntegerField(verbose_name="Coins", default=0)
    transaction_charges = models.PositiveIntegerField(verbose_name="Transaction Charges", default=0)
    # // PositiveIntegerField - An integer. Values from 0 to 2147483647 - 2.4 billion
    # // PositiveBigIntegerField -  0 to 9223372036854775807 - 9,223 quadrillion (9 x10^18)
    last_login          = models.DateTimeField(verbose_name="Last Login", blank=True, null=True)
    date_joined         = models.DateTimeField(verbose_name="Date Joined", blank=False)
    time_code           = models.PositiveIntegerField(verbose_name="Time Code", default=0)
    # time_code is All Time Code, which may become One Day Code later
    is_active           = models.BooleanField(default=True)
    is_admin            = models.BooleanField(default=False)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)


    USERNAME_FIELD = 'account_id'
    REQUIRED_FIELDS = []
    # REQUIRED_FIELDS = ['identification', ]

    objects = AccountManager()


    def __str__(self):
        return self.account_id

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True




