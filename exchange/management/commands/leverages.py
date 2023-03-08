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
            if 'USDT' in item.symbol :
                try:
                    coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
                    coin = coinex.margin_config(market =  item.symbol)
                    item.leverage = (coin['leverage'])
                    item.buymin = (coin[item.symbol.replace('USDT' , '')]['min_amount'])
                    item.buymax = (coin[item.symbol.replace('USDT' , '')]['max_amount'])
                    item.sellmin =(coin['USDT']['min_amount'])
                    item.sellmax =(coin['USDT']['max_amount'])
                    item.save()
                except:
                    item.delete()
            elif 'BTC' in item.symbol :
                try:
                    coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
                    coin = coinex.margin_config(market =  item.symbol)
                    item.leverage = (coin['leverage'])
                    item.buymin = (coin[item.symbol.replace('BTC' , '')]['min_amount'])
                    item.buymax = (coin[item.symbol.replace('BTC' , '')]['max_amount'])
                    item.sellmin =(coin['BTC']['min_amount'])
                    item.sellmax =(coin['BTC']['max_amount'])
                    item.save()
                except:
                    item.delete()