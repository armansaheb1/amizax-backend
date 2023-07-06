from typing import Text
from django.utils import timezone
from django.db.models import manager
from requests.sessions import Request
from requests import get
from exchange.views import cp_withdraw, currencies, currency, notifications, price, usersinfo
from django.shortcuts import get_object_or_404, render
from django import http
from django.db.models.fields import EmailField
from .lib.coinex import CoinEx
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from exchange.serializers import  BottomStickerSerializer, BuySerializer, BuyoutSerializer, Cp_WithdrawSerializer, CpDepositRequestSerializer, CpWalletSerializer, ExchangeSerializer, GeneralSerializer, LevelFeeSerializer, PerpetualRequestSerializer, PostsSerializer, ProfitSerializer, SellSerializer, TopStickerSerializer, VerifyAcceptRequestSerializer, VerifyMelliRequest , BankAccountsSerializer, StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer, WithdrawSerializer, selloutSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from exchange.models import BottomSticker, Cp_Currencies, Cp_Wallet, Cp_Withdraw, CpDepositRequest, General, LevelFee, News, Notification, Perpetual, PerpetualRequest, Posts ,  Price, ProfitList, Review, Staff, TopSticker,  UserInfo , Currencies, VerifyAcceptRequest, VerifyBankAccountsRequest, VerifyBankRequest, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest, WithdrawRequest, buyoutrequest, buyrequest, exchangerequest, selloutrequest, sellrequest
from django.contrib.auth.models import AbstractUser , User
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
import json as jj
from datetime import datetime ,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from ippanel import Client
import pytz
from random import randrange
from django.db.models import Q

def sendemail(user , date = '' , title = '' , text = '') :
    send_mail(
        'Subject here',
        f'{title}\n{text}',
        'info@ramabit.com',
        [f'{user.email}'],
        fail_silently=False,
    )

def sms(user , date = False , text = False , pattern='gf9zbtg61v'):
    sms = Client("qsVtNKDEKtFZ9wgS4o1Vw81Pjt-C3m469UJxCsUqtBA=")

    if pattern == 'r4hxan3byx' or pattern == 'tfpvvl8beg'  :
        pattern_values = {
    "text": text,
    }
    else :
        pattern_values = {
    "name": "کاربر",
    }

    bulk_id = sms.send_pattern(
        f"{pattern}",    # pattern code
        "+983000505",      # originator
        f"+98{UserInfo.objects.get(user = user).mobile}",  # recipient
        pattern_values,  # pattern values
    )

    message = sms.get_message(bulk_id)
    print(message)
    print(f"+98999999999")
    return True

def notification (user , date = datetime.now(), title = '' , text = '',pattern='gf9zbtg61v'):
    note = Notification(user = user , title = title , text = text)
    note.save()
    try:
        sms(user=user , text=text , pattern=pattern)
    except:
        pass
    sendemail(user=user  , date=date, title=title, text = text)

class staff(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return Staff.objects.filter(user = user)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        staff =  self.get_object(request.user)
        serializer = StaffSerializer(staff , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if Staff.objects.get(user = request.user).level < 3 :
            return Response(status= status.HTTP_400_BAD_REQUEST)
        if len(Staff.objects.filter(user = request.user))<1:
            serializer = StaffSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.error, status= status.HTTP_400_BAD_REQUEST)
        else:
            serializer = Staff.objects.get(user = request.data['id'])
            serializer.level = request.data['level']
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request ,user, format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        users = []
        userinfo =  User.objects.filter(username=user)
        for item in userinfo :
            if len(UserInfo.objects.filter(user = item)) > 0:
                userinfos = UserInfo.objects.get(user = item)
                wallet= 0
                price = 0
                for itemm in Wallet.objects.filter(user = item):
                    if itemm.currency.id == 1:
                        wallet = itemm.amount
                users.append({'username': item.username, 'level': userinfos.level, 'balance': wallet, 'is_active': userinfos.is_active, 'is_admin': item.is_staff, 'id': item.id })
        return Response(users)
    def post(self , request , format=None):
        user = UserInfo.objects.get(user = User.objects.get(id = request.data['id']))
        if request.data['act'] == 1:
            if user.is_active == True:
                user.is_active = False
            elif user.is_active == False:
                user.is_active = True
        user.save()
        return Response(status=status.HTTP_201_CREATED)

class userinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request ,user , format=None):
        query = UserInfo.objects.filter(user = user )
        serializer = UserInfoSerializer(query , many= True)
        return Response(serializer.data ,status=status.HTTP_201_CREATED)

class USDTP(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        query = General.objects.get(id = 1 )
        return Response({'USDTp':query.USDTpercent , 'USDTp2':query.USDTpercent2, 'USDTp3':query.USDTpercent3, 'sellpercent': query.sellpercent})

    def post(self, request , format=None):
        query = General.objects.get(id = 1 )
        query.USDTpercent = request.data['USDTp']
        query.USDTpercent2 = request.data['USDTp2']
        query.USDTpercent3 = request.data['USDTp3']
        query.sellpercent = request.data['sellpercent']
        query.save()
        return Response(query.USDTpercent)

class users(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        users = []
        userinfo =  User.objects.all().order_by('id')
        for item in userinfo :
            if len(UserInfo.objects.filter(user = item)) > 0:
                userinfos = UserInfo.objects.get(user = item)
                wallet= 0
                price = 0
                for itemm in Wallet.objects.filter(user = item):
                    if itemm.currency.id == 1:
                        wallet = itemm.amount
                users.append({'username': item.username, 'level': userinfos.level, 'balance': wallet, 'is_active': userinfos.is_active, 'is_admin': item.is_staff, 'id': item.id })
        return Response(users)
    def post(self , request , format=None):
        user = UserInfo.objects.get(user = User.objects.get(id = request.data['id']))
        if request.data['act'] == 1:
            if user.is_active == True:
                user.is_active = False
            elif user.is_active == False:
                user.is_active = True
        user.save()
        return Response(status=status.HTTP_201_CREATED)

class bankcards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankRequest.objects.all()
        serializer = VerifyBankRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response({'message': 'not admin'}, status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response({'message': 'not admin'}, status= status.HTTP_400_BAD_REQUEST)
        request.data['user'] = VerifyBankRequest.objects.get(id = request.data['id']).user.id
        serializer = BankCardsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            VerifyBankRequest.objects.get(id = request.data['id']).delete()
            verify = Verify.objects.get(user = request.data['user'])
            verify.bankv = True
            verify.save()
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                user = UserInfo.objects.get(user = request.data['user'])
                user.level = 1
                user.save()
                notification(user = user.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyBankRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class cards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankRequest.objects.filter(user = request.data['user'])
        serializer = VerifyBankRequestSerializer(bankcards , many=True)
        return Response(serializer.data)


class cp_wallet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request ,id, format=None):
        coinex = CoinEx(Perpetual.objects.get(user=User.objects.get(id =id)).apikey, Perpetual.objects.get(user=User.objects.get(id =id)).secretkey)
        res = coinex.balance_info()
        result = {}
        for item in Cp_Currencies.objects.all():
            if len(Cp_Wallet.objects.filter(currency = item , user= request.user)):
                wal = Cp_Wallet.objects.get(currency = item , user= request.user)
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':wal.balance}
            else: 
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':'0'}
        return Response(result)

class cp_history(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request, id , format=None):
        if id == 'all':
            coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')
            res = coinex.sub_account_transfer_history()
            return Response(res)
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')
        res = coinex.sub_account_transfer_history(sub_user_name= Perpetual.objects.get(user=User.objects.get(id = id)).name)
        print(res)
        return Response(res)

class bankaccounts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyBankAccountsRequest.objects.all()
        serializer = VerifyBankAccountsRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        request.data['user'] = VerifyBankAccountsRequest.objects.get(id = request.data['id']).user.id
        serializer = BankAccountsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            id = request.data['id']
            req = VerifyBankAccountsRequest.objects.get(id = id)
            ver = Verify.objects.get(user = req.user)
            ver.accountv = True
            ver.save()
            verify = Verify.objects.get(user = req.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                user = UserInfo.objects.get(user = req.user)
                user.level = 1
                user.save()
                notification(user = user.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            req = VerifyBankAccountsRequest.objects.get(id = id)
            req.delete()
            return Response(status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyBankAccountsRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)

class verify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        return Verify.objects.filter(user = user)
            
    def get(self , request, user , format=None):
        verify = self.get_object(user)
        serializer = VerifySerializer(verify , many=True)
        return Response(serializer.data)

class verifymelli(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyMelliRequest.objects.filter(action = False)
        serializer = VerifyMelliRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        verify = Verify.objects.get(user = request.data['user'])
        verify.melliv = True
        verify.save()
        if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
            user = UserInfo.objects.get(user = request.data['user'])
            user.level = 1
            user.save()
            notification(user = user.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
        id = request.data['id']
        req = VerifyMelliRequest.objects.get(id = id)
        req.action = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyMelliRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)
 
class verifyaccept(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = VerifyAcceptRequest.objects.filter(action = False)
        serializer = VerifyAcceptRequestSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        verify = Verify.objects.get(user = request.data['user'])
        verify.acceptv = True
        verify.save()
        if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                user = UserInfo.objects.get(user = request.data['user'])
                user.level = 1
                user.save()
                notification(user = user.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
        id = request.data['id']
        req = VerifyAcceptRequest.objects.get(id = id)
        req.action = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)


    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = VerifyAcceptRequest.objects.get(id = id)
        req.delete()
        return Response(status=status.HTTP_201_CREATED)


class cwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(rejected = False , completed = False)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = Cp_Withdraw.objects.get(id = id)
        user = req.user.id
        notification(user = User.objects.get(id = user) , title = 'درخواست برداشت وجه شما انجام شد' , text = f'درخواست برداشت مقدار  {req.amount} و ارسال آن به آدرس  {req.address} با موفقیت انجام شد ')
        req.completed = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)
 
    def put(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        req = Cp_Withdraw.objects.get(id = id)
        user = req.user.id
        notification(user = User.objects.get(id = user) , title = ' متاسفانه درخواست برداشت وجه شما انجام نشد ' , text = f'درخواست برداشت مقدار  {req.amount} و ارسال آن به آدرس  {req.address}  با مشکل روبرو شد . لطفا با پشتیبانی تماس بگیرید ')
        req.rejected = True
        req.save()
        return Response(status=status.HTTP_201_CREATED)

class rcwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(rejected = True)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)

class ccwithdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        bankcards = Cp_Withdraw.objects.filter(completed = True)
        serializer = Cp_WithdrawSerializer(bankcards , many=True)
        return Response(serializer.data)


class general(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = General.objects.filter(id = 1)
        serializer = GeneralSerializer(query , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        gen = General.objects.get(id = 1)
        if 'name' in request.data :
            gen.name = request.data['name']
        if 'email' in request.data :
            gen.email = request.data['email']
        if 'telephone' in request.data :
            gen.telephone = request.data['telephone']
        if 'instagram' in request.data :
            gen.instagram = request.data['instagram']
        if 'telegram' in request.data :
            gen.telegram = request.data['telegram']
        if 'whatsapp' in request.data :
            gen.whatsapp = request.data['whatsapp']
        if 'rule' in request.data :
            gen.rule = request.data['rule']
        if 'logo' in request.data :
            gen.logo = request.data['logo']
        gen.save()
        return Response(status=status.HTTP_201_CREATED)

class perpetualreq(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = PerpetualRequest.objects.all()
        serializer = PerpetualRequestSerializer(query , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        query = PerpetualRequest.objects.filter(id = id)
        serializer = PerpetualRequestSerializer(query , many=True)
        return Response(serializer.data)

class perpetualreqccept(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)
        id = request.data['id']
        user = PerpetualRequest.objects.get(id = id).user
        if not len(Perpetual.objects.filter(user = user)):
            per = Perpetual(user = user ,name = request.data['name'], apikey = request.data['apikey'] , secretkey = request.data['secretkey'])
            per.save()
        else : 
            per = Perpetual.objects.get(user = user)
            per.name = request.data['name'], 
            per.apikey = request.data['apikey'] , 
            per.secretkey = request.data['secretkey']
            per.save()
        ver = Verify.objects.get(user = user)
        ver.coinv = True
        ver.save()
        verify = Verify.objects.get(user = user)
        if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                user = UserInfo.objects.get(user = user)
                user.level = 1
                user.save()
                notification(user = user.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
        pe = PerpetualRequest.objects.get(id = id)
        pe.delete()
        return Response(status=status.HTTP_201_CREATED)


class subject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Subjects.objects.all()

    def get(self , request , format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)

        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self, request, id, format=None):
        if len(Staff.objects.filter(user = request.user))<1:
            return Response(status= status.HTTP_400_BAD_REQUEST)
        else:
            if Staff.objects.get(user = request.user).level < 1 :
                return Response(status= status.HTTP_400_BAD_REQUEST)

        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  Subjects.objects.filter(id = id)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        request.data['user'] = User.objects.get(username = request.data['username']).id
        sub = Subjects(user = request.user , title = request.data['title'])
        sub.save()
        request.data['user'] = request.user.id
        request.data['subid'] = sub.id
        serializer = TicketsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ticket(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , id):
        return Tickets.objects.filter(subid = id)

    def get(self , request , id , format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = TicketsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = TicketsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class transactions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        try:
            return Transactions.objects.all()
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        transactions = self.get_object(request.user)
        serializer = TransactionsSerializer(transactions , many=True)
        return Response(serializer.data)

class withdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self, request , format=None):
        serializer = WithdrawSerializer(WithdrawRequest.objects.filter(act = 0), many = True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
        
    def post(self, request , format=None):
        wr = WithdrawRequest.objects.get(id = request.data['id'])
        tr = Transactions(user = wr.user , amount = wr.amount , currency =Currencies.objects.get(id=1), act = 2)
        tr.save()
        wr.act = 1
        wr.save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, id , format=None):
        wr = WithdrawRequest.objects.get(id = id)
        wa = Wallet.objects.get(user = wr.user , currency = Currencies.objects.get(id = 1))
        wa.amount = wa.amount + wr.amount
        wa.save()
        wr.delete()
        return Response(status=status.HTTP_201_CREATED)

class topsticker(APIView):
    def get(self , request , format=None):
        pages = Pages.objects.filter(position = 'top')
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request, id, format=None):
        serializer = Pages.objects.get(id = id)
        serializer.delete()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        post = Pages.objects.get(id=request.data['id'])
        post.text = request.data['text']
        post.minitext = request.data['minitext']
        post.title = request.data['title']
        if 'pic' in request.data:
            print(request.data)
            post.pic = request.data['pic']
        post.save()
        return Response(status=status.HTTP_201_CREATED)

class bottomsticker(APIView):
    def get(self , request , format=None):
        pages = Pages.objects.filter(position = 'bottom')
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request, id, format=None):
        serializer = Pages.objects.get(id = id)
        serializer.delete()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        post = Pages.objects.get(id=request.data['id'])
        post.text = request.data['text']
        post.minitext = request.data['minitext']
        post.title = request.data['title']
        if 'pic' in request.data:
            print(request.data)
            post.pic = request.data['pic']
        post.save()
        return Response(status=status.HTTP_201_CREATED)


class mainpageposts(APIView):
    def get(self , request , format=None):
        pages = Pages.objects.filter(position = 'mainposts')
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request, id, format=None):
        serializer = Pages.objects.get(id = id)
        serializer.delete()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        post = Pages.objects.get(id=request.data['id'])
        post.text = request.data['text']
        post.minitext = request.data['minitext']
        post.title = request.data['title']
        if 'pic' in request.data:
            print(request.data)
            post.pic = request.data['pic']
        post.save()
        return Response(status=status.HTTP_201_CREATED)


class otherpages(APIView):
    def get(self , request , format=None):
        pages = Pages.objects.filter(position = 'others')
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request, id, format=None):
        serializer = Pages.objects.get(id = id)
        serializer.delete()
        return Response(status=status.HTTP_201_CREATED)

class editotherpages(APIView):

    def post(self , request , format=None):
        post = Pages.objects.get(id=request.data['id'])
        post.text = request.data['text']
        post.title = request.data['title']
        if 'pic' in request.data:
            print(request.data)
            post.pic = request.data['pic']
        post.save()
        return Response(status=status.HTTP_201_CREATED)

class details(APIView):
    def get(self , request , format=None):
        pages = Pages.objects.filter(position = 'details')
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request, id, format=None):
        serializer = Pages.objects.get(id = id)
        serializer.delete()
        return Response(status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        post = Pages.objects.get(id=request.data['id'])
        post.text = request.data['text']
        post.title = request.data['title']
        post.save()
        return Response(status=status.HTTP_201_CREATED)

class wallets(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return Wallet.objects.filter(user = User.objects.get(username= user))
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request, username , format=None):
        userinfo = self.get_object(user = username)
        serializer = WalletSerializer(userinfo , many=True)
        return Response(serializer.data)


class levelchange(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
            
    def post(self , request , format=None):
        userinfo = UserInfo.objects.get(user = User.objects.get(username = request.data['username']))
        userinfo.level = int(request.data['level'])
        userinfo.save()
        return Response(status=status.HTTP_201_CREATED)
        

class changepass(APIView):
    def post(self , request):
        user = User.objects.get(username = request.data['username'])
        passw = request.data['pass']
        passs = make_password(str(passw))
        user.password = passs
        user.save()
        return Response(status=status.HTTP_201_CREATED)

class review(APIView):
    def get(self, request):
        hours = 0
        days = 0
        weeks = 0
        months = 0
        for item in Review.objects.all():
            if item.date > timezone.now() - timedelta(hours = 1):
                hours = hours + 1
            if item.date > timezone.now() - timedelta(days = 1):
                days = days + 1
            if item.date > timezone.now() - timedelta(weeks = 1):
                weeks = weeks + 1
            if item.date > timezone.now() - timedelta(weeks = 4):
                months = months + 1
        return Response({'days': days,'weeks': weeks, 'months': months, 'hours': hours })

class profit_rial(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]


    def get_object(self, user):
        return ProfitList.objects.filter(currency = 'ریال').order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ProfitSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class buy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        if request.data['act'] == 'reject':
            req = buyrequest.objects.get(id = request.data['id'])
            wal = Wallet.objects.get(user= req.user , currency = Currencies.objects.get(id = 1))
            wal.amount = wal.amount + req.ramount
            wal.save()
            note = Notification(user=req.user, title = 'خرید نا موفق' , text = 'متاسفانه درخواست خرید شما با مشکل مواجه شده . لطفا با پشتیبانی تماس بگیرید')
            note.save()
            req.act = 1
            req.save()
            return Response(status=status.HTTP_201_CREATED)
        req = buyrequest.objects.get(id = request.data['id'])
        profit = ProfitList(user = req.user , amount = (int(req.ramount) - int(request.data['rramount'])), currency = 'ریال' , operation = f'{req.currency}خرید')
        profit.save()
        note = Notification(user=req.user, title = 'خرید موفق' , text = ' درخواست خرید شما با موفقیت انجام شد . ')
        note.save()
        req.act = 2
        req.save()
        return Response( status=status.HTTP_201_CREATED)

class exchange(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return exchangerequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ExchangeSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        if request.data['act'] == 'reject':
            req = exchangerequest.objects.get(id = request.data['id'])
            note = Notification(user=req.user, title = 'اکسچینج نا موفق' , text = 'متاسفانه درخواست اکسچینج شما با مشکل مواجه شده . لطفا با پشتیبانی تماس بگیرید')
            note.save()
            req.act = 1
            req.save()
            return Response(status=status.HTTP_201_CREATED)
        req = exchangerequest.objects.get(id = request.data['id'])
        note = Notification(user=req.user, title = 'اکسچینج موفق' , text = ' درخواست اکسچینج شما با موفقیت انجام شد . ')
        note.save()
        req.act = 2
        req.save()
        return Response( status=status.HTTP_201_CREATED)

class exchangedone(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return exchangerequest.objects.filter(act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ExchangeSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class exchangereject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return exchangerequest.objects.filter(act = 1).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ExchangeSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class cp_deposit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return CpDepositRequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = CpDepositRequestSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        if request.data['act'] == 'reject':
            req = CpDepositRequest.objects.get(id = request.data['id'])
            note = Notification(user=req.user, title = 'شارژ حساب نا موفق' , text = 'متاسفانه درخواست شارژ حساب شما با مشکل مواجه شده . لطفا با پشتیبانی تماس بگیرید')
            note.save()
            req.act = 1
            req.save()
            return Response(status=status.HTTP_201_CREATED)
        req = CpDepositRequest.objects.get(id = request.data['id'])
        note = Notification(user=req.user, title = 'شارژ حساب موفق' , text = ' درخواست شارژ حساب شما با موفقیت انجام شد . ')
        note.save()
        req.act = 2
        req.save()
        return Response( status=status.HTTP_201_CREATED)

class cp_depositdone(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return CpDepositRequest.objects.filter(act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = CpDepositRequestSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class cp_depositreject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return CpDepositRequest.objects.filter(act = 1).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = CpDepositRequestSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class buydone(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.filter(act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sell(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return sellrequest.objects.filter(act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = SellSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        req = buyrequest.objects.get(id = request.data['id'])
        profit = ProfitList(user = req.user , amount = (int(request.data['rramount']) - int(req.ramount)), currency = 'ریال' , operation = f'{req.currency}فروش')
        profit.save()
        req.act = 3
        return Response( status=status.HTTP_201_CREATED)

class selldone(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return sellrequest.objects.filter(~Q(act = 0)).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = SellSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class buyreject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.filter(act = 1).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class buyout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyoutrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuyoutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        if request.data['act'] == 'reject':
            req = buyoutrequest.objects.get(id = request.data['id'])
            wal = Wallet.objects.get(user= req.user , currency = Currencies.objects.get(id = 1))
            wal.amount = wal.amount + req.ramount
            wal.save()
            note = Notification(user=req.user, title = 'خرید نا موفق' , text = 'متاسفانه درخواست خرید شما با مشکل مواجه شده . لطفا با پشتیبانی تماس بگیرید')
            note.save()
            req.act = 1
            req.save()
            return Response(status=status.HTTP_201_CREATED)
        req = buyoutrequest.objects.get(id = request.data['id'])
        profit = ProfitList(user = req.user , amount = (float(req.ramount) - float(request.data['rramount'])) , currency = 'ریال' , operation = f'{req.currency} خرید خارجی')
        profit.save()
        note = Notification(user=req.user, title = 'خرید موفق' , text = ' درخواست خرید شما با موفقیت انجام شد . ')
        note.save()
        req.act = 2
        req.save()
        return Response( status=status.HTTP_201_CREATED)

class sellout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return selloutrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = selloutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    def post(self , request, format=None):
        if request.data['act'] == 'reject':
            req = selloutrequest.objects.get(id = request.data['id'])
            note = Notification(user=req.user, title = 'خرید نا موفق' , text = 'متاسفانه درخواست خرید شما با مشکل مواجه شده . لطفا با پشتیبانی تماس بگیرید')
            note.save()
            req.act = 1
            req.save()
            return Response(status=status.HTTP_201_CREATED)
        req = selloutrequest.objects.get(id = request.data['id'])
        if len(Wallet.objects.filter(user = req.user , currency = Currencies.objects.get( id = 1))):
            wall = Wallet.objects.get(user = req.user , currency = Currencies.objects.get( id = 1))
            wall.amount = wall.amount + float(req.ramount)
            wall.save()
        else:
            wa = Wallet(user = req.user , currency = Currencies.objects.get( id = 1) , amount = float(req.amount))
            wa.save()
        profit = ProfitList(user = req.user , amount = (float(request.data['rramount']) - float(req.ramount)), currency = 'ریال' , operation = f'{req.currency} فروش خارجی')
        profit.save()
        note = Notification(user=req.user, title = 'خرید موفق' , text = ' درخواست خرید شما با موفقیت انجام شد . ')
        note.save()
        req.act = 2
        req.save()
        return Response( status=status.HTTP_201_CREATED)

class selloutopen(APIView):
    def get_object(self, user):
        return selloutrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = selloutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
class buyoutopen(APIView):
    def get_object(self, user):
        return buyoutrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuyoutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sellouthistory(APIView):
    def get_object(self, user):
        return selloutrequest.objects.filter(~Q(act = 0)).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = selloutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class buyouthistory(APIView):
    def get_object(self, user):
        return buyoutrequest.objects.filter(~Q(act = 0)).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuyoutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)



class sellopen(APIView):
    def get_object(self, user):
        return sellrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = SellSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
class buyopen(APIView):
    def get_object(self, user):
        return buyrequest.objects.filter(act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sellhistory(APIView):
    def get_object(self, user):
        return sellrequest.objects.filter(~Q(act = 0)).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = SellSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)
class buyhistory(APIView):
    def get_object(self, user):
        return buyrequest.objects.filter(~Q(act = 0)).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)



class levelfee(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = LevelFee.objects.all().order_by('id')
        serializer = LevelFeeSerializer(user , many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LevelFee.objects.get(id = request.data['id'])
        serializer.buy = request.data['buy']
        serializer.sell = request.data['sell']
        serializer.perpetual = request.data['perpetual']
        serializer.margin = request.data['margin']
        serializer.exchange = request.data['exchange']
        serializer.save()
        return Response( status=status.HTTP_201_CREATED)


