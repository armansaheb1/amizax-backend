from exchange.views import currency
from exchange.models import Leverage, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        Lev = Leverage.objects.all()
        for item in Lev:
            if 'چین'in item.symbol:
                item.symbol = item.symbol.replace('چین' , '')
                item.save()
            if 'پروتکل'in item.symbol:
                item.symbol = item.symbol.replace('پروتکل' , '')
                item.save()