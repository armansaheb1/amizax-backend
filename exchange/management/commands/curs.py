from exchange.views import currency
from exchange.models import Cp_Currencies, Leverage, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
from django.core.management.base import BaseCommand, CommandError
import requests
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        for itemm in Cp_Currencies.objects.all():
            itemm.delete()
        r = requests.get(url = 'https://api.coinex.com/v1/common/asset/config').json()
        list = r['data'].keys()
        for item in list :
            lev = Cp_Currencies(name=item, brand = r['data'][item]['asset'], chain = r['data'][item]['chain'], can_deposit = r['data'][item]['can_deposit'], can_withdraw = r['data'][item]['can_withdraw'], deposit_least_amount = r['data'][item]['deposit_least_amount'] , withdraw_least_amount = r['data'][item]['withdraw_least_amount'] , withdraw_tx_fee = r['data'][item]['withdraw_tx_fee'] )
            lev.save()