from exchange.models import Perpetual, PerpetualRequest, Staff,  UserInfo , Currencies, VerifyBankAccountsRequest, VerifyBankRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.core.management.base import BaseCommand, CommandError
from cryptos import *

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Verify.objects.all():
            if len(PerpetualRequest.objects.filter(user= item.user)) < 1:
                pe = PerpetualRequest(user = item.user)
                pe.save()
            if len(Perpetual.objects.filter(user=item.user)) > 0:
                for itemm in PerpetualRequest.objects.filter(user= item.user):
                    itemm.delete()
            if len(VerifyBankAccountsRequest.objects.filter(user=item.user)) > 1:
                for a in range(len(VerifyBankAccountsRequest.objects.filter(user=item.user)) - 1):
                    VerifyBankAccountsRequest.objects.filter(user=item.user)[0].delete()

            if len(VerifyBankRequest.objects.filter(user=item.user)) > 1:
                for a in range(len(VerifyBankRequest.objects.filter(user=item.user)) - 1):
                    VerifyBankRequest.objects.filter(user=item.user)[0].delete()