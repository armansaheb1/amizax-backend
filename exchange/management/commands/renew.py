from exchange.models import Perpetual, Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest
import requests
from bit import Key
from django.core.management.base import BaseCommand, CommandError
from cryptos import *
from .lib import CoinexPerpetualApi
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in Perpetual.objects.all():
            coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
            print(item.name)
            result = coinex.apis(item.name)['data'][0]['user_auth_id']
            result = coinex.renew(result , item.name)
            print(result)
            result = coinex.apis(item.name)['data'][0]
            print(result)
        return
