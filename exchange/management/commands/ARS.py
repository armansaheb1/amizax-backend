from exchange.views import currency
from exchange.models import Leverage, Price , Staff,  UserInfo , Currencies , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest, transactionid
from django.core.management.base import BaseCommand, CommandError
import requests
from .lib import CoinexPerpetualApi
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    robot = CoinexPerpetualApi('130F31B38E6146DE96A96925C1238AB3','2AA13CE30B30A1EE6798243154A4C1C5104A006BF6E8F0F8')
    robot.adjust_leverage(position_type=2, market= 'ADAUSDT', leverage= '5')
    coinex = CoinEx('130F31B38E6146DE96A96925C1238AB3', '2AA13CE30B30A1EE6798243154A4C1C5104A006BF6E8F0F8' )
    status = 'nodeal'
    coinex = CoinEx('130F31B38E6146DE96A96925C1238AB3', '2AA13CE30B30A1EE6798243154A4C1C5104A006BF6E8F0F8' )
    coin = robot.get_market_state(
        'ADAUSDT',
    )
    averagechange = float(coin['data']['ticker']['buy']) * 0.002
    aver = float(coin['data']['ticker']['buy']) * 0.001
    step = averagechange
    lastprice = float(coin['data']['ticker']['buy'])
    lastprice2 = float(coin['data']['ticker']['buy'])
    mintrade = str(1 / float(coin['data']['ticker']['buy']))
    tradesp = []
    tradesn = []
    def handle(self, *args, **options):
        def trader():
            while True:
                coin2 = self.robot.get_market_state(
                    'ADAUSDT',
                )
                price = float(coin2['data']['ticker']['buy'])
                if self.status == 'nodeal':
                    self.status = 'sdeal'
                    self.lastprice = price
                    self.lastprice2 = price

                elif self.status == 'pdeal':
                    list = self.robot.query_position_pending(
                            'ADAUSDT',
                        )
                    count = len(list['data'])
                    if price > self.lastprice + self.step:
                        
                        print('----pdeal+')
                        try:
                            tr = self.robot.put_market_order(
                                market = 'ADAUSDT',
                                side = 1,
                                amount = 5
                            )
                            self.tradesp.append(tr['data']['position_id'])
                        except:
                            pass
                        self.lastprice = price
                        self.lastprice2 = price
                    elif price > self.lastprice2:
                            self.lastprice2 = price
                            print('increased')
                    elif price < self.lastprice2 - (self.aver):
                        print('----pdeal-')
                        list = self.robot.query_position_pending(
                            'ADAUSDT',
                        )
                        for item in list['data']:
                            tr = self.robot.close_market(
                                'ADAUSDT',
                                int(item['position_id'])
                            )
                        self.tradesp = []
                        self.status = 'sdeal'


                elif self.status == 'ndeal':
                    list = self.robot.query_position_pending(
                            'ADAUSDT',
                        )
                    count = len(list['data'])
                    if price < self.lastprice - self.step:
                        print('----ndeal+')
                        if len(self.tradesn) < 3:
                        
                            try:
                                tr = self.robot.put_market_order(
                                    market = 'ADAUSDT',
                                    side = 2,
                                    amount = 5
                                )
                                self.tradesn.append(tr['data']['position_id'])
                            except:
                                pass
                            self.lastprice = price
                            self.lastprice2 = price
                            
                        elif price < self.lastprice2:
                            self.lastprice2 = price
                            print('decreased')
                    elif price > self.lastprice2 + (self.aver):
                        print('----ndeal-')
                        list = self.robot.query_position_pending(
                            'ADAUSDT',
                        )
                        for item in list['data']:
                            tr = self.robot.close_market(
                                'ADAUSDT',
                                int(item['position_id'])
                            )
                        self.tradesn = []
                                
                        self.status = 'sdeal'
                else:


                    if price > self.lastprice + self.aver:
                        if len(self.tradesn) < 3:
                            try:
                                tr = self.robot.put_market_order(
                                    market = 'ADAUSDT',
                                    side = 1,
                                    amount = 5
                                )
                                self.tradesp.append(tr['data']['position_id'])
                            except:
                                pass
                            self.status = 'pdeal'
                            self.lastprice = price
                            self.lastprice2 = price
                    elif price < self.lastprice - (self.aver * 1.5):
                        try:
                            tr = self.robot.put_market_order(
                                market = 'ADAUSDT',
                                side = 2,
                                amount = 5
                            )
                            self.tradesn.append(tr['data']['position_id'])
                        except:
                            pass
                        self.status = 'ndeal'
                        self.lastprice = price
                        self.lastprice2 = price
                time.sleep(1)
                tran = ''
                trap = ''
                for item in self.tradesn:
                    tran = tran + str(item) + '-'
                for item in self.tradesp:
                    trap = trap + str(item) + '-'
                print(self.status + '   ' + 'n =' + tran + '   ' + 'p =' + trap )
        trader()