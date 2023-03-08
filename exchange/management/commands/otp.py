from exchange.models import Perpetual, PerpetualRequest, Staff,  UserInfo , Currencies, VerifyBankAccountsRequest, VerifyBankRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.core.management.base import BaseCommand, CommandError
from cryptos import *
import pyotp
import base32_lib 

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in UserInfo.objects.all():
            item.otp = base32_lib.generate(length=16, checksum=True)
            item.save()