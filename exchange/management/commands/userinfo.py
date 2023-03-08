from exchange.models import Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.contrib.auth.models import AbstractUser , User, UserManager
from django.core.management.base import BaseCommand, CommandError
from cryptos import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in User.objects.all():
            if len(UserInfo.objects.filter(user = item))<1:
                ui = UserInfo(user = item,first_name='',last_name='')
                ui.save()