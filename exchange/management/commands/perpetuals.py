from exchange.models import Perpetual, PerpetualRequest, Staff,  UserInfo , Currencies, VerifyBankAccountsRequest, VerifyBankRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Perpetual.objects.all():
            pass