from requests.sessions import Request
from django.contrib.auth.hashers import check_password
from exchange.lib import request_client
from rest_framework.generics import GenericAPIView
from rest_framework import mixins
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError
from typing import Text
from django import http
from django.http import response
import datetime
import requests
from .lib.request_client import RequestClient
from .lib.coinex import CoinEx
import time
from django.db.models.fields import EmailField
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import request, serializers
from django.http import HttpResponse , Http404 
from rest_framework import status
from rest_framework import authentication
from .serializers import BottomStickerSerializer, BuySerializer, BuyoutSerializer, CpCurrenciesSerializer, CpDepositRequestSerializer, CpWalletSerializer, ExchangeSerializer, GeneralSerializer, LevelFeeSerializer, LeverageSerializer, NewsSerializer, PostsSerializer, ProTradesBuyOrderSerializer, ProTradesSellOrderSerializer , MainTradesBuyOrderSerializer, MainTradesSellOrderSerializer, ProTradesSerializer, MainTradesSerializer, NotificationSerializer, BankAccountsSerializer, SellSerializer, TopStickerSerializer, VerifyAcceptRequestSerializer, VerifyBankAccountsRequest , PriceSerializer , StaffSerializer, UserInfoSerializer, VerifyBankAccountsRequestSerializer, VerifyMelliRequestSerializer , WalletSerializer , CurrenciesSerializer ,VerifySerializer, BankCardsSerializer, TransactionsSerializer, SettingsSerializer, SubjectsSerializer, TicketsSerializer, PagesSerializer , UserSerializer , ForgetSerializer, VerifyBankRequestSerializer, WithdrawSerializer, selloutSerializer, Oltrade4Serializer, AlertSerializer, P2pRequestSerializer, ChainSerializer, ChatRoomSerializer, ChatTextSerializer, P2pBuyRequestSerializer
from rest_framework.views import APIView 
from rest_framework.response import Response
from .models import BottomSticker, General, Indexprice , Cp_Currencies, Cp_Wallet, Cp_Withdraw, LevelFee, Leverage, News, Perpetual, PerpetualRequest, Posts, PriceHistory, ProfitList, Referal, Review, SmsVerified, TopSticker, VerifyAcceptRequest, buyapp, buyoutrequest, buyrequest, exchangerequest, mobilecodes, ProTradesSellOrder, MainTradesSellOrder,ProTradesBuyOrder, MainTradesBuyOrder, ProTrades, MainTrades, Notification , VerifyBankAccountsRequest , BankAccounts, Price, Staff,  UserInfo , Currencies, VerifyMelliRequest , Wallet , Verify , BankCards, Transactions, Settings, Subjects, Tickets, Pages , Forgetrequest , VerifyBankRequest, selloutrequest, sellrequest, Transactionid, Alert, P2pRequest, ChatRoom, ChatText, P2pBuyRequest, SmsCode
from django.contrib.auth.models import AbstractUser , User, UserManager
from django.contrib.auth.decorators import user_passes_test
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
import uuid
import json
from datetime import datetime ,timedelta
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from ippanel import Client
import pytz
from random import randrange
import requests
from itertools import chain
import secrets
import logging
import copy
import hashlib
import time
import traceback
from .lib import CoinexPerpetualApi
from django.db.models import Q
from sarafi.settings import ROOT
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json
from django.utils import timezone

def sendemail(user , date = '' , title = '' , text = '') :
    try:
        send_mail(
            'Subject here',
            f'{title}\n{text}',
            'info@ramabit.com',
            [f'{user.email}'],
            fail_silently=False,
        )
    except:
        pass

def sms(user , date = False , text = False , pattern = 'gf9zbtg61v'):
    try:
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
    except:
        pass

def notification (user , date = '', title = '' , text = '', pattern='gf9zbtg61v'):
    note = Notification(user = user , title = title , text = text)
    note.save()
    try:
        sms(user = user , pattern= pattern)
    except Exception: 
        pass
    sendemail(user = user , text = text , title= title)

class timeout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        if request.user.is_authenticated:
            if UserInfo.objects.get(user = request.user).last_visit < timezone.now() - timedelta(minutes=30):
                return Response(True)
            else:
                # Update last visit time after request finished processing.
                use = UserInfo.objects.get(user=request.user)
                use.last_visit=timezone.now()
                use.save()
            return Response(False)
        return Response(False)

class login(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        utc=pytz.UTC
        if len(User.objects.filter(username = request.data['username']))>0:
            if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))>0:
                if UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).smsverify:
                    if SmsVerified.objects.filter(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile):
                        ver = SmsVerified.objects.get(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile)
                        ver.delete()
                        data = {}
                        username = request.data['username']
                        print(username)
                        password = request.data['password']
                        try:
                            Account = User.objects.get(username=username)
                        except BaseException as e:
                            return Response({f'{str(e)}'} , status=status.HTTP_400_BAD_REQUEST)
                        token = Token.objects.get_or_create(user=Account)[0].key
                        print(token)
                        if not check_password(password, Account.password):
                            return Response({"رمز عبور اشتباه است"} , status=status.HTTP_400_BAD_REQUEST)
                        if Account:
                            if Account.is_active:
                                print(request.user)
                                data["message"] = "user logged in"
                                data["username"] = Account.email
                                Res = {"data": data, "auth_token": token}
                                if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))>0:
                                    if UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile:
                                        notification(user = User.objects.get(username = request.data['username']), title='Amizax', text = 'با موفقیت به حساب خود وارد شدید' ,  pattern='gf9zbtg61v')
                                if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))<1:
                                    ui = UserInfo(user = User.objects.get(username = request.data['username']),first_name='',last_name='')
                                    ui.save()
                                    notification(user = User.objects.get(username = request.data['username']), title='Amizax', text = 'با موفقیت به حساب خود وارد شدید' , pattern='gf9zbtg61v')
                                use = UserInfo.objects.get(user=Account)
                                use.last_visit=timezone.now()
                                use.save()
                                return Response(Res)
                            else:
                                return Response({"حساب شما مسدود شده است"} , status=status.HTTP_400_BAD_REQUEST)

                        else:
                            return Response({"حسابی با این مشخصات یافت نشد "} , status=status.HTTP_400_BAD_REQUEST)
                    else:
                        vcode = randrange(123456,999999)
                        a = mobilecodes.objects.filter(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile)
                        for item in a:
                            item.delete()
                        c = mobilecodes(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile, code = vcode)
                        c.save()
                        sms = Client("qsVtNKDEKtFZ9wgS4o1Vw81Pjt-C3m469UJxCsUqtBA=")

                        pattern_values = {
                        "verification-code": f"{vcode}",
                        }

                        bulk_id = sms.send_pattern(
                            "s1a8zjq33u",    # pattern code
                            "+983000505",      # originator
                            f"+98{UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile}",  # recipient
                            pattern_values,  # pattern values
                        )

                        message = sms.get_message(bulk_id)
                        return Response(1)
                else:
                    data = {}
                    username = request.data['username']
                    print(username)
                    password = request.data['password']
                    try:

                        Account = User.objects.get(username=username)
                    except BaseException as e:
                        return Response({f'{str(e)}'} , status=status.HTTP_400_BAD_REQUEST)
                    token = Token.objects.get_or_create(user=Account)[0].key
                    print(token)
                    if not check_password(password, Account.password):
                        return Response({"رمز عبور اشتباه است"} , status=status.HTTP_400_BAD_REQUEST)

                    if Account:
                        if Account.is_active:
                            print(request.user)
                            data["message"] = "user logged in"
                            data["username"] = Account.username

                            Res = {"data": data, "auth_token": token}
                            if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))>0:
                                if UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile:
                                    notification(user = User.objects.get(username = request.data['username']), title='Amizax',text = 'با موفقیت به حساب خود وارد شدید', pattern='gf9zbtg61v')
                            if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))<1:
                                ui = UserInfo(user = User.objects.get(username = request.data['username']),first_name='',last_name='')
                                ui.save()
                                notification(user = User.objects.get(username = request.data['username']), title='Amizax',text = 'با موفقیت به حساب خود وارد شدید', pattern='gf9zbtg61v')
                            use = UserInfo.objects.get(user=Account)
                            use.last_visit=timezone.now()
                            use.save()
                            return Response(Res)

                        else:
                            return Response({"حساب شما مسدود شده است"} , status=status.HTTP_400_BAD_REQUEST)

                    else:
                        return Response({"حسابی با این مشخصات یافت نشد "} , status=status.HTTP_400_BAD_REQUEST)
            else:
                data = {}
                username = request.data['username']
                print(username)
                password = request.data['password']
                try:

                    Account = User.objects.get(username=username)
                except BaseException as e:
                    return Response({f'{str(e)}'} , status=status.HTTP_400_BAD_REQUEST)
                token = Token.objects.get_or_create(user=Account)[0].key
                print(token)
                if not check_password(password, Account.password):
                    return Response({"رمز عبور اشتباه است"} , status=status.HTTP_400_BAD_REQUEST)

                if Account:
                    if Account.is_active:
                        print(request.user)
                        data["message"] = "user logged in"
                        data["username"] = Account.username

                        Res = {"data": data, "auth_token": token}
                        if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))>0:
                            if UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile:
                                notification(user = User.objects.get(username = request.data['username']), title='Amizax',text = 'با موفقیت به حساب خود وارد شدید', pattern='gf9zbtg61v')
                        if len(UserInfo.objects.filter(user = User.objects.get(username = request.data['username'])))<1:
                            ui = UserInfo(user = User.objects.get(username = request.data['username']),first_name='',last_name='',phone='')
                            ui.save()
                            notification(user = User.objects.get(username = request.data['username']), title='Amizax',text = 'با موفقیت به حساب خود وارد شدید', pattern='gf9zbtg61v')
                        use = UserInfo.objects.get(user=Account)
                        use.last_visit=timezone.now()
                        use.save()
                        return Response(Res)

                    else:
                        return Response({"حساب شما مسدود شده است"} , status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"حسابی با این مشخصات یافت نشد "} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"حسابی با این مشخصات یافت نشد "} , status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class loginsms(APIView):
    def post(self, request, format=None):
        
        c = mobilecodes.objects.get(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile)
        if(int(request.data['code']) == int(c.code)):
            smss = SmsVerified.objects.filter(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile)
            for item in smss:
                item.delete()
            sms = SmsVerified(number = UserInfo.objects.get(user = User.objects.get(username = request.data['username'])).mobile)
            sms.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)

class addreferal(APIView):
    def post(self, request, format=None):
            ref = Referal(inviting = User.objects.get(username = request.data['username']) , inviter = UserInfo.objects.get(referalid = request.data['referal']).user)
            ref.save()
            return Response(status=status.HTTP_200_OK)

class welcomesms(APIView):
    def get(self, request, format=None):
            notification(user = request.user, title='Amizax', text='خود وارد شدید Amizax با موفقیت به حساب  ')
            return Response(status=status.HTTP_200_OK)
    

NP_MERCHANT = '5a273bf9-c01e-48bd-abd2-816563ad61cc'
NP_API_REQUEST = "https://nextpay.org/nx/gateway/token"
NP_API_VERIFY = "https://nextpay.org/nx/gateway/verify"
NP_CallbackURL = 'https://amizax.com/api/v1/verifys2/'
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید" 
email = 'email@example.com'  
mobile = '09123456789'  


class createsmscode(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not len(SmsCode.objects.filter(user = request.user, date__gte= datetime.now() - timedelta(minutes = 2))):
            for item in SmsCode.objects.filter(user = request.user):
                item.delete()
            vcode = randrange(123456,999999)
            sc = SmsCode.objects.create(number = vcode, user= request.user)
            sc.save()
            sms = Client("qsVtNKDEKtFZ9wgS4o1Vw81Pjt-C3m469UJxCsUqtBA=")

            pattern_values = {
            "verification-code": f"{vcode}",
            }

            bulk_id = sms.send_pattern(
                "s1a8zjq33u",    # pattern code
                "+983000505",      # originator
                f"+98{UserInfo.objects.get(user = request.user).mobile}",  # recipient
                pattern_values,  # pattern values
            )

            message = sms.get_message(bulk_id)
            return Response()
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)




class send_next(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        amount = int(request.data['amount'])/10
        uid = str(uuid.uuid4())
        
        payload='api_key=5a273bf9-c01e-48bd-abd2-816563ad61cc&amount=' +str(amount)+ '&order_id=&customer_phone=&callback_uri=' + NP_CallbackURL + '&allowed_card=' + str(request.data['card'])
        headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        trans = requests.request("POST", NP_API_REQUEST, headers=headers, data=payload).json()
        tr = Transactionid(user = request.user , transid = uid , amount = int(request.data['amount']), tid = trans['trans_id'])
        tr.save()
        if not trans['trans_id']:
            return HttpResponse(trans['code']) 
        return Response(f"https://nextpay.org/nx/gateway/payment/{trans['trans_id']}")


MERCHANT = '2a4c4e4e-3e4c-431f-80f5-3b5172b763c2'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید" 
email = 'email@example.com'  
mobile = '09123456789'  
CallbackURL = 'https://amizax.com/api/v1/verifys/'

class send_request(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        uid = str(uuid.uuid4())
        tr = Transactionid(user = request.user , transid = uid , amount = int(request.data['amount']))
        tr.save()
        req_data = {
            "merchant_id": MERCHANT,
            "amount": int(request.data['amount']),
            "callback_url": CallbackURL + uid ,
            "description": description,
            "metadata": {"mobile": mobile, "email": email, "card_pan":str(request.data['card']) ,}
        }
        req_header = {"accept": "application/json",
                    "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return HttpResponse(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

class send_request2(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        CallbackURL2 = 'https://amizax.com/api/v1/buyappback/'
        uid = str(uuid.uuid4())
        amount = 0
        if int(request.data['option']) == 1:
            amount = 300000000
        elif int(request.data['option']) == 2:
            amount = 400000000
        elif int(request.data['option']) == 3:
            amount = 500000000
        tr = Transactionid(user = request.user , transid = uid , amount = amount)
        tr.save()
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": CallbackURL2 + uid ,
            "description": description,
            "metadata": {}
        }
        req_header = {"accept": "application/json",
                    "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return HttpResponse(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")

def verifys(request, transid):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    transactioni = Transactionid.objects.get(transid = transid)
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": transactioni.amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                user = transactioni.user
                if len(Wallet.objects.filter(user = user , currency = Currencies.objects.get(id = 1))) > 0:
                    wallet = Wallet.objects.get(user = user , currency = Currencies.objects.get(id = 1))
                    wallet.amount = wallet.amount + int(transactioni.amount)
                    wallet.save()
                else:
                    wa = Wallet(user = user , currency = Currencies.objects.get(id = 1), amount = int(transactioni.amount))
                    wa.save()
                tra = Transactions(user = user, amount= transactioni.amount, act = 1, currency = Currencies.objects.get(id = 1))
                tra.save()
                return redirect('https://amizax.com/success')
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')

def verifys2(request):
    tid = request.GET.get('trans_id', '')
    transactioni = Transactionid.objects.get(tid = tid)
    amount = request.GET.get('amount', '')
    payload='api_key=5a273bf9-c01e-48bd-abd2-816563ad61cc&amount='+str(amount)+ f'&trans_id={tid}'
    headers = {
    'User-Agent': 'PostmanRuntime/7.26.8',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", NP_API_VERIFY, headers=headers, data=payload).json()
    if int(response['code']) == 0:
        user = transactioni.user
        if len(Wallet.objects.filter(user = user , currency = Currencies.objects.get(id = 1))) > 0:
            wallet = Wallet.objects.get(user = user , currency = Currencies.objects.get(id = 1))
            wallet.amount = wallet.amount + int(transactioni.amount)
            wallet.save()
        else:
            wa = Wallet(user = user , currency = Currencies.objects.get(id = 1), amount = int(transactioni.amount))
            wa.save()
        tra = Transactions(user = user, amount= transactioni.amount, act = 1, currency = Currencies.objects.get(id = 1))
        tra.save()
        return redirect('https://amizax.com/success')
    elif int(response['code']) == '-6':
        return render(request, 'failure.html', {'message': 'کارت استفاده شد همخوانی ندارد'})
    else:
        return render(request, 'failure.html', {'message': 'خطایی رخ داده است'})

def buyappback(request, transid):
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    transactioni = Transactionid.objects.get(transid = transid)
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": transactioni.amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                user = transactioni.user
                if int(transactioni.amount) == 300000000:
                    type = 1
                elif int(transactioni.amount) == 400000000:
                    type = 2
                elif int(transactioni.amount) == 500000000:
                    type = 3
                buyapp(user = user , type = type)
                return redirect('https://amizax.com/success')
            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


class rulev(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        ver = Verify.objects.get(user=request.user)
        ver.rulev = True
        ver.save()
        verify = Verify.objects.get(user= request.user)
        if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
            per = UserInfo.objects.get(user = request.user)
            per.level = 1
            per.save()
            notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
        return Response(status=status.HTTP_201_CREATED)

class general(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [AllowAny]

    def get(self , request , format=None):
        query = General.objects.get()
        serializer = GeneralSerializer(query)
        return Response(serializer.data)

class usersinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return UserInfo.objects.get(user = user)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        if len(Notification.objects.filter(user = request.user)) < 1 : 
            note = Notification(user = request.user , title = 'خوش آمدید' , text = 'به AMIZAX خوش آمدید') 
            note.save()
        userinfo =  self.get_object(request.user)
        serializer = UserInfoSerializer(userinfo)
        return Response(serializer.data)
    
    def post(self, request , format=None):
        if len(UserInfo.objects.filter(user = request.user)) < 1:
            u = UserInfo(user = request.user, first_name = request.data['first_name'], last_name = request.data['last_name'], address = request.data['address'] ,postal = request.data['postal'] )
            u.save()
            ver = Verify.objects.get(user = request.user)
            ver.idv = True
            ver.save() 
            verify = Verify.objects.get(user= request.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                per = UserInfo.objects.get(user = request.user)
                per.level = 1
                per.save()
            notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            note = Notification(user = request.user , title = ' اطلاعات شما با موفقیت ثبت شد' , text = 'برای شروع معاملات لطفا احراز هویت را انجام دهید') 
            note.save()
            return Response( status=status.HTTP_201_CREATED)
        else:
            user = UserInfo.objects.get(user = request.user)
            user.first_name = request.data['first_name']
            user.last_name = request.data['last_name']
            user.save()
            ver = Verify.objects.get(user = request.user)
            ver.idv = True
            ver.save() 
            verify = Verify.objects.get(user= request.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                per = UserInfo.objects.get(user = request.user)
                per.level = 1
                per.save()
                notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            return Response( status=status.HTTP_201_CREATED)

    def put(self, request , format=None):
        user = UserInfo.objects.get(user = request.user)
        if 'smsverify' in request.data:
            user.smsverify = bool(request.data['smsverify'])
        if 'googleverify' in request.data:
            user.googleverify = bool(request.data['googleverify'])
        if 'emailverify' in request.data:
            user.emailverify = bool(request.data['emailverify'])
        user.save()
        return Response( status=status.HTTP_201_CREATED)

        
class addphone(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self, request , format=None):
        user = UserInfo.objects.get(user = request.user)
        user.phone = request.data['phonenum']
        user.save()
        return Response( status=status.HTTP_201_CREATED)

class dashboardinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        item = User.objects.get(id= request.user.id)
        if len(UserInfo.objects.filter(user = item)) > 0:
                userinfos = UserInfo.objects.get(user = item)
                wallet= 0
                wallets= []
                usbalance = 0
                r2 = requests.get(url = 'https://api.coinex.com/v1/common/currency/rate')
                r2 = float(r2.json()['data']['USDT_to_USD'])  + float(r2.json()['data']['USDT_to_USD']) * General.objects.get(id =1).USDTpercent2 / 100
                r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
                lists = r.json()['data']['ticker']
                for itemm in Cp_Wallet.objects.filter(user=request.user):
                    if itemm.currency.brand == 'USDT':
                        usbalance = usbalance + ((1)* itemm.balance)
                    else:
                        usbalance = usbalance + ((float(lists[itemm.currency.brand + 'USDT']['last']))* itemm.balance)
                price = 0
                users=[]
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = 1))) > 0:
                    wallet = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 1)).amount
                userinfos = UserInfo.objects.get(user = request.user)
                openorder = len(MainTradesBuyOrder.objects.filter(user = request.user)) + len(MainTradesSellOrder.objects.filter(user = request.user)) + len(ProTradesBuyOrder.objects.filter(user = request.user)) + len(ProTradesSellOrder.objects.filter(user = request.user))
                opens = list(chain(MainTradesBuyOrder.objects.filter(user = request.user), MainTradesSellOrder.objects.filter(user = request.user), ProTradesBuyOrder.objects.filter(user = request.user), ProTradesSellOrder.objects.filter(user = request.user)))
                openorders = MainTradesSellOrderSerializer(opens , many=True).data
                unread = 0 
                for items in Subjects.objects.filter(user = request.user):
                    if not items.read :
                        unread = unread + 1
                users.append({'username': item.username, 'level': userinfos.level, 'balance': wallet, 'is_active': userinfos.is_active, 'is_admin': userinfos.is_admin, 'id': item.id, 'openorder': openorder, 'unread': unread, 'openorders': openorders, 'wallets': wallets, 'usbalance': usbalance})
        return Response(users)

class user(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        try:
            return User.objects.filter(id = user.id)
        except UserInfo.DoesNotExist:
            return Http404

    def get(self , request , format=None):
        userinfo =  self.get_object(request.user)
        serializer = UserSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        userinfo =  User.objects.all()
        serializer = UserSerializer(userinfo , many=True)
        return Response(serializer.data)


class price(APIView):


            
    def get(self , request , format=None):
        price = Price.objects.get(id=1)
        price.rial = price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent / 100))
        price.save()
        price = Price.objects.filter(id=1)
        serializer = PriceSerializer(price , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class leverages(APIView):
            
    def get(self , request , format=None):
        price = Leverage.objects.all()
        list={}
        for item in price :
            list[f'{item.symbol}'] = {'leverage': item.leverage, 'bmin': item.buymin, 'bmax': item.buymax, 'smin': item.sellmin, 'smax': item.sellmax}
        return Response(list , status=status.HTTP_201_CREATED)



class pricehistory(APIView):
            
    def get(self , request , format=None):
        pricehis = {'rial': [],'btc': [],'eth': [],'trx': [],'usdt': [],'doge': [],'usd': [], }
        price = PriceHistory.objects.all().order_by('-id')[:7]
        for item in price:
            pricehis['rial'].append(item.rial)
            pricehis['btc'].append(item.btc)
            pricehis['eth'].append(item.eth)
            pricehis['trx'].append(item.trx)
            pricehis['usdt'].append(item.usdt)
            pricehis['doge'].append(item.doge)
            pricehis['usd'].append(item.usd)
        return Response(pricehis , status=status.HTTP_201_CREATED)


class wallets(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return Wallet.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        userinfo = self.get_object(request.user.id)
        serializer = WalletSerializer(userinfo , many=True)
        return Response(serializer.data)


class wallet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user , id):
        try:
            return Wallet.objects.filter(user = user , currency = Currencies.objects.get(id = id))
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , id):
        userinfo = self.get_object(request.user , id)
        serializer = WalletSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self ,request , id):
        if id == 5 :
            url = "https://api.trongrid.io/wallet/generateaddress"
            headers = {"Accept": "application/json"}
            response = requests.request("GET", url, headers=headers)
            print(response.json())
            address = response.json()['Address']
            key = response.json()['privateKey']
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)
        if id == 2 :
            hd_wallet_fact = HdWalletFactory(HdWalletCoins.BITCOIN)
            hd_wallet = hd_wallet_fact.CreateRandom("my_wallet_name", HdWalletWordsNum.WORDS_NUM_12)
            hd_wallet.Generate(addr_num = 1)
            walls = hd_wallet.ToDict()['addresses']['address_1']
            key = walls['wif_priv']
            address =  walls['address']
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)

        if id == 3 :
            priv = secrets.token_hex(32)
            private_key = "0x" + priv
            acct = Account.from_key(private_key)
            address = acct.address
            key = private_key
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)
        if id == 6 :
            seed = Wal.generate_mnemonic()
            w = Wal.create_wallet(network="DOGE", seed=seed, children=1)
            address = w['address']
            key = w['wif']
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                wa = Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))
                wa.key = key
                wa.address = address
                wa.save()
            else:
                wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                wa.save()
            return Response(status=status.HTTP_201_CREATED)

        if id == 4 :
            if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = 5))) > 0 :
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).key
                    wa.address = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).address
                    wa.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).address , key = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 5)).key)
                    wa.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                url = "https://api.shasta.trongrid.io/wallet/generateaddress"
                headers = {"Accept": "application/json"}
                response = requests.request("GET", url, headers=headers)
                print(response.json())
                address = response.json()['address']
                key = response.json()['privateKey']
                if len(Wallet.objects.filter(user = request.user , currency = Currencies.objects.get(id = id))) > 0:
                    wa = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = id))
                    wa.key = key
                    wa.address = address
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 5) , amount = 0 , address = address , key = key)
                    wa2.save()
                else:
                    wa = Wallet(user = request.user , currency = Currencies.objects.get(id = id) , amount = 0 , address = address , key = key)
                    wa.save()
                    wa2 = Wallet(user = request.user , currency = Currencies.objects.get(id = 5) , amount = 0 , address = address , key = key)
                    wa2.save()
                return Response(status=status.HTTP_201_CREATED)



class currency(APIView):
    def get_object(self , id):
        try:
            return Currencies.objects.filter(id = id)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request ,id):
        userinfo = self.get_object(id)
        serializer = CurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)

class currencies(APIView):

    def get_object_all(self):
        try:
            return Currencies.objects.all().order_by('id')
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request):
        userinfo = self.get_object_all()
        serializer = CurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)


class verify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        if(len(Verify.objects.filter(user = user))<1):
            verif = Verify(user = user)
            verif.save()
        try:
            return Verify.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        verify = self.get_object(request.user)
        serializer = VerifySerializer(verify , many=True)
        return Response(serializer.data)

class bankcards(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return BankCards.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        bankcards = self.get_object(request.user)
        serializer = BankCardsSerializer(bankcards , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        serializer = VerifyBankRequest(user = request.user, bankc = request.data['bankc'])
        for item in VerifyBankRequest.objects.filter(bankc = request.data['bankc']):
            item.delete()
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class bankaccounts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        try:
            return BankAccounts.objects.filter(user = user)
        except BankAccounts.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        bankaccounts = self.get_object(request.user)
        serializer = BankAccountsSerializer(bankaccounts , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyBankAccountsRequestSerializer(data = request.data)
        if serializer.is_valid():
            for item in VerifyBankAccountsRequest.objects.filter(shebac = request.data['shebac']):
                item.delete()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class transactions(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self , user):
        try:
            return Transactions.objects.filter(user = user)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        transactions = self.get_object(request.user)
        serializer = TransactionsSerializer(transactions , many=True)
        return Response(serializer.data)


class settings(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get_object(self):
        try:
            return Settings.objects.filter(id = 1)
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        settings = self.get_object()
        serializer = SettingsSerializer(settings , many=True)
        return Response(serializer.data)

    def put(self , request , format=None):
        request.data['id'] = 1
        serializer = Settings.objects.get(id=1)
        serializer.data = request.data
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class pages(APIView):
    
    def get_object(self):
        try:
            return Pages.objects.all()
        except Wallet.DoesNotExist:
            return Http404
            
    def get(self , request , format=None):
        pages = self.get_object()
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)

class addforget(APIView):
    def post(self , request , format=None):
        if(len(User.objects.filter(email = request.data['email']))<1):
            return Response({
            'error' : 'کاربر با ایمیل وارد شده یافت نشد'
        }, status=status.HTTP_404_NOT_FOUND)
        serializer = ForgetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = request.data['email']
            key = Forgetrequest.objects.filter(email = email).reverse()[0].key
            response_data = {}
            response_data['result'] = 'Create post successful!'
            send_mail(
            'Subject here',
            f' ',
            'info@ramabit.com',
            [f'{email}'],
            fail_silently=False,
        )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class resetpass(APIView):
    def get(self , request ,key, format=None):
        utc=pytz.UTC
        
        if(Forgetrequest.objects.get(key = key).date + timedelta(minutes = 10) > utc.localize(datetime.now())):
            return redirect(f"http://localhost:8080/resetpass/{key}")
        else:
            return redirect(f"http://localhost:8080/expired")

    def post(self , request):
        key = request.data['key']
        if(len(Forgetrequest.objects.filter(key = request.data['key']))<1):
            return redirect(f"http://localhost:8080/expired")
        user = User.objects.get(email = Forgetrequest.objects.get(key = request.data['key']).email)
        passw = request.data['password']
        repassw = request.data['repassword']
        if passw == repassw:
            passs = make_password(str(passw))
            user.password = passs
            user.save()
            return redirect(f"http://localhost:8080/login")

class mobileverify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def put(self , request):
        if len(UserInfo.objects.filter(mobile = request.data['number'])) and not UserInfo.objects.get(mobile = request.data['number']).user == request.user:
            return Response('حساب دیگری با این شماره ثبت شده است', status=status.HTTP_400_BAD_REQUEST)
        if not 'number' in request.data:
            request.data['number'] = UserInfo.objects.get(user = request.user).mobile
        vcode = randrange(123456,999999)
        a = mobilecodes.objects.filter(number = request.data['number'])
        for item in a:
            item.delete()
        c = mobilecodes(number = request.data['number'], code = vcode)
        c.save()

        sms = Client("qsVtNKDEKtFZ9wgS4o1Vw81Pjt-C3m469UJxCsUqtBA=")

        pattern_values = {
        "verification-code": f"{vcode}",
        }

        bulk_id = sms.send_pattern(
            "s1a8zjq33u",    # pattern code
            "+983000505",      # originator
            f"+98{request.data['number']}",  # recipient
            pattern_values,  # pattern values
        )

        message = sms.get_message(bulk_id)
        print(message)
        print(f"+98{request.data['number']}")
        return Response(status=status.HTTP_200_OK )

    def post(self , request):
        user = Verify.objects.get(user= request.user)
        c = mobilecodes.objects.get(number= request.data['number'])
        if(int(request.data['code']) == int(c.code)):
            user.mobilev = True
            user.save()
            mobile = UserInfo.objects.get(user = request.user)
            mobile.mobile = request.data['number']
            mobile.save()
            verify = Verify.objects.get(user = request.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                per = UserInfo.objects.get(user = request.user)
                per.level = 1
                per.save()
                notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)

class regemailverify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request):
        user = Verify.objects.get(user= User.objects.get(username = request.data['username']))
        vcode = randrange(123456, 999999)
        user.emailc = vcode
        user.save()
        
        send_mail(
            'Subject here',
            f'به شرکت سرمایه گذاری Amizax خوش آمدید کد فعالسازی : /n برای تایید حساب خود روی لینک زیر کلیک کنید /n https://www.amizax.com/api/v1/email/{vcode} ',
            'info@ramabit.com',
            [f'{request.data["email"]}'],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)

    def get(self , request ,code ):
        user = Verify.objects.get(user= request.user)
        if(int(code) == int(user.emailc)):
            user.emailv = True
            user.save()
            mail = request.user
            mail.email = request.data['email']
            mail.save()
            verify = Verify.objects.get(user = request.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                per = UserInfo.objects.get(user = request.user)
                per.level = 1
                per.save()
                notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)


class emailverify(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def put(self , request):
        user = Verify.objects.get(user= request.user)
        vcode = randrange(123456, 999999)
        user.emailc = vcode
        user.save()
        
        send_mail(
            'Subject here',
            f'به شرکت سرمایه گذاری Amizax خوش آمدید کد فعالسازی : {vcode} ',
            'info@ramabit.com',
            [f'{request.data["email"]}'],
            fail_silently=False,
        )
        return Response(status=status.HTTP_200_OK)

    def post(self , request):
        user = Verify.objects.get(user= request.user)
        if(int(request.data['code']) == int(user.emailc)):
            user.emailv = True
            user.save()
            mail = request.user
            mail.email = request.data['email']
            mail.save()
            verify = Verify.objects.get(user = request.user)
            if verify.bankv and verify.melliv and verify.mobilev and verify.emailv and verify.acceptv and verify.coinv and verify.accountv :
                per = UserInfo.objects.get(user = request.user)
                per.level = 1
                per.save()
                notification(user = request.user ,title='Amizax',text='حساب شما با موفقیت تایید شد',date= datetime.now() , pattern= 'qiep09qzea')
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "کد وارد شده معتبر نیست"} , status=status.HTTP_400_BAD_REQUEST)

class verifymelli(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyMelliRequestSerializer(data = request.data)
        if serializer.is_valid():
            for item in VerifyMelliRequest.objects.filter(user = request.user):
                item.delete()
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class verifyaccept(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        serializer = VerifyAcceptRequestSerializer(data = request.data)
        if serializer.is_valid():
            for item in VerifyAcceptRequest.objects.filter(user = request.user):
                item.delete()
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class bankrequests(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user):
        return VerifyBankRequest.objects.filter(user = user)

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = VerifyBankRequestSerializer(userinfo , many=True)
        return Response(serializer.data)

class notifications(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Notification.objects.filter(user = user)

    def get(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = NotificationSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        for item in userinfo :
            item.seen = True
            item.save()
            return Response(status=status.HTTP_201_CREATED)

class subject(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , user):
        return Subjects.objects.filter(user = user).order_by('date')

    def get(self , request , format=None):
        userinfo =  self.get_object(request.user)
        serializer = SubjectsSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        request.data['user'] = request.user.id
        sub = Subjects(user = request.user , title = request.data['title'])
        sub.save()
        request.data['subid'] = sub.id
        serializer = TicketsSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self , request , format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        for item in userinfo :
            item.read = True
            item.save()
            return Response(status=status.HTTP_201_CREATED)

class ticket(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self , id):
        return Tickets.objects.filter(subid = id)

    def get(self , request , id , format=None):
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

class maintrades(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return MainTrades.objects.all()

    def get(self , request , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object()
        serializer = MainTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  MainTrades.objects.filter(brand = id)
        serializer = MainTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

class protrades(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return ProTrades.objects.all()

    def get(self , request , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object()
        serializer = ProTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

    def post(self , request, id , format=None):
        if len(self.get_object()) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  ProTrades.objects.filter(id = id)
        serializer = ProTradesSerializer(userinfo , many=True)
        return Response(serializer.data)

class fasttorial(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get(self , request , id , format=None):
        uprice = price = Price.objects.get(id = 1).usd
        if (Currencies.objects.get(id = id).brand == 'BTC'):
            price = Price.objects.get(id = 1).btc
        if (Currencies.objects.get(id = id).brand == 'ETH'):
            price = Price.objects.get(id = 1).eth
        if (Currencies.objects.get(id = id).brand == 'USDT'):
            price = Price.objects.get(id = 1).usdt
        if (Currencies.objects.get(id = id).brand == 'TRX'):
            price = Price.objects.get(id = 1).trx
        if (Currencies.objects.get(id = id).brand == 'DOGE'):
            price = Price.objects.get(id = 1).doge
        wallet = Wallet.objects.get(user=request.user , currency = Currencies.objects.get(id = id))
        amount = wallet.amount
        return Response({'price': price*amount*uprice} , status=status.HTTP_201_CREATED)

    def post(self , request , id , format=None):
        uprice = price = Price.objects.get(id = 1).usd
        if (Currencies.objects.get(id = id).brand == 'BTC'):
            price = Price.objects.get(id = 1).btc
        if (Currencies.objects.get(id = id).brand == 'ETH'):
            price = Price.objects.get(id = 1).eth
        if (Currencies.objects.get(id = id).brand == 'USDT'):
            price = Price.objects.get(id = 1).usdt
        if (Currencies.objects.get(id = id).brand == 'TRX'):
            price = Price.objects.get(id = 1).trx
        if (Currencies.objects.get(id = id).brand == 'DOGE'):
            price = Price.objects.get(id = 1).doge
        wallet = Wallet.objects.get(user=request.user , currency = Currencies.objects.get(id = id))
        amount = wallet.amount
        ramount = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 1))
        ramount.amount += price*amount*uprice
        ramount.save()
        wallet.amount = 0
        wallet.save()
        return Response(status=status.HTTP_201_CREATED)

class maintradebuyorders(APIView):

    def get_object(self , id):
        return MainTradesBuyOrder.objects.filter(trade = MainTrades.objects.get(brand = id), status = False)

    def get(self, request, id, format=None):
        userinfo =  self.get_object(id)
        serializer = MainTradesBuyOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request ,id , format=None):
        amount = float(request.data['amount'])
        price = float(request.data['price'])
        sells = MainTradesSellOrder.objects.filter(price__lte = request.data['price'] , trade = MainTrades.objects.get(brand = id) , status= False).order_by('-price')
        i=0
        if not len(Wallet.objects.filter(user = request.user , currency = MainTrades.objects.get(brand = id).scurrency)):
            return Response({
            'error' : "موجودی کافی نیست"
            }, status=status.HTTP_400_BAD_REQUEST)
        wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(brand = id).scurrency)
        if amount * price > wal2.amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        wal2.amount = wal2.amount - (amount * price)
        wal2.save()
        add = MainTradesBuyOrder(trade = MainTrades.objects.get(brand = id) ,user = request.user, amount = amount , price = price, left = amount)
        add.save()
        if len(sells) > 0 :
            if not len(Cp_Wallet.objects.filter(user = request.user , currency = MainTrades.objects.get(brand = id).bcurrency)):
                cc = Cp_Wallet(user = request.user , currency = MainTrades.objects.get(brand = id).bcurrency)
                cc.save()
            wal3 = Cp_Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(brand = id).bcurrency)
            while i < len(sells) and amount > 0:
                item = sells[i]
                wal = Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(brand = id).scurrency)
                if amount < item.left :
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal3.balance = wal3.balance + amount
                    wal3.save()
                    item.left = item.left - amount
                    item.save()
                    add.left = add.left - amount
                    add.status = True
                    add.save()
                    amount = 0
                elif amount == item.left :
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal3.balance = wal3.balance + amount
                    wal3.save()
                    item.left = item.left - amount
                    item.status = True
                    item.save()
                    add.left = add.left - amount
                    add.status = True
                    add.save()
                    amount = 0
                else :
                    wal.amount = wal.amount + (amount * item.price)
                    wal.save()
                    wal3.balance = wal3.balance + amount
                    wal3.save()
                    add.left = add.left - item.left
                    add.save()
                    item.left = item.left - amount
                    item.status = True
                    item.save()
                    amount = amount - item.left
                i = i +1
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_201_CREATED)
    

class maintradesellorders(APIView):

    def get_object(self , id):
        return MainTradesSellOrder.objects.filter(trade = MainTrades.objects.get(brand = id), status = False)

    def get(self, request, id, format=None):
        userinfo =  self.get_object(id)
        serializer = MainTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request, id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        buys = MainTradesBuyOrder.objects.filter(price__gte = request.data['price'], trade = MainTrades.objects.get(brand = id), status= False).order_by('price')
        i=0
        if not len(Cp_Wallet.objects.filter(user = request.user , currency = MainTrades.objects.get(brand = id).bcurrency)):
            return Response({
            'error' : "موجودی کافی نیست"
            }, status=status.HTTP_400_BAD_REQUEST)
        wal3 = Cp_Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(brand = id).bcurrency)
        if amount > wal3.balance :
            return Response({
            'error' : "موجودی کافی نیست"
            }, status=status.HTTP_400_BAD_REQUEST)
        if not(Wallet.objects.filter(user = request.user , currency = MainTrades.objects.get(brand = id).scurrency)):
            ww = Wallet(user = request.user , currency = MainTrades.objects.get(brand = id).scurrency)
            ww.save()
        wal2 = Wallet.objects.get(user = request.user , currency = MainTrades.objects.get(brand = id).scurrency)
        wal3.balance = wal3.balance - amount
        wal3.save()
        add = MainTradesSellOrder(trade = MainTrades.objects.get(brand = id) ,user = request.user, amount = amount , price = price, left = amount)
        add.save()
        if len(buys) > 0 :
            while (i < len(buys)) and (amount > 0):
                item = buys[i]
                wal = Cp_Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(brand = id).bcurrency)
                if amount < item.left :
                    wal.balance = wal.balance + amount
                    wal.save()
                    wal2.amount = wal2.amount + (amount * item.price)
                    wal2.save()
                    item.left = item.left - amount
                    item.save()
                    add.left = add.left - amount
                    add.status = True
                    add.save()
                    amount = 0

                elif amount == item.left :
                    wal = Cp_Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(brand = id).bcurrency)
                    wal.balance = wal.balance + amount
                    wal.save()
                    wal2.amount = wal2.amount + (amount * item.price)
                    wal2.save()
                    item.left = item.left - amount
                    item.status = True
                    item.save()
                    add.left = add.left - amount
                    add.status = True
                    add.save()
                    amount = 0
                
                elif amount > item.left :

                    wal = Cp_Wallet.objects.get(user = item.user , currency = MainTrades.objects.get(brand = id).bcurrency)
                    wal.balance = wal.balance + amount
                    wal.save()
                    wal2.amount = wal2.amount + (amount * item.price)
                    wal2.save()
                    add.left = add.left - item.left
                    add.save()
                    item.left = item.left - amount
                    item.status = True
                    item.save()
                    amount = amount - item.left
                    i = i +1
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_201_CREATED)


class maintradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        return MainTrades.objects.get(brand = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        sbalance = 0
        bbalance = 0
        minsell = 0
        maxbuy = 0
        if len(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            minsell = MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')[0].price
        if len(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            maxbuy = MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')[0].price
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        if(len(Cp_Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Cp_Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).balance
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer,status=status.HTTP_201_CREATED)

class maintradesselllist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return MainTradesSellOrder.objects.filter(user = user)

    def get(self , request, format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = MainTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)

class maintradesbuylist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return MainTradesBuyOrder.objects.filter(user = user)

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = MainTradesBuyOrderSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class protradebuyorders(APIView):

    def get_object(self , id):
        return ProTradesBuyOrder.objects.filter(trade = ProTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = ProTradesBuyOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request ,id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        sells = ProTradesSellOrder.objects.filter(price__lte = request.data['price'] , trade = ProTrades.objects.get(id = id)).order_by('-price')
        i=0
        if amount * price > Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(sells) > 0 :
            while i < len(sells) or amount == 0:
                item = sells[i]
                if amount < item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    item.delete()
                    amount = 0

                else :

                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal.amount = wal.amount + (amount * item.price)
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal.save()
                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount - (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount + amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
            if amount > 0 :
                add = ProTradesBuyOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
                add.save()
                wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                wal3.amount = wal3.amount + amount
                wal3.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = ProTradesBuyOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
            add.save()
            wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
            wal3.amount = wal3.amount + amount
            wal3.save()
            return Response(status=status.HTTP_201_CREATED)
    

class protradesellorders(APIView):

    def get_object(self , id):
        return ProTradesSellOrder.objects.filter(trade = ProTrades.objects.get(id = id))

    def get(self, request, id, format=None):
        if len(self.get_object(id)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(id)
        serializer = ProTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)
    
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self , request, id , format=None):
        amount = float(request.data['amount'])
        amountstart = float(request.data['amount'])
        price = float(request.data['price'])
        trade = id
        user = request.user
        buys = ProTradesBuyOrder.objects.filter(price__gte = request.data['price'], trade = ProTrades.objects.get(id = trade)).order_by('price')
        i=0
        if amount > Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency).amount :
            return Response({
            'error' : "موجودی کافی نیست"
        }, status=status.HTTP_400_BAD_REQUEST)
        if len(buys) > 0 :
            while i < len(buys) or amount == 0:
                item = buys[i]
                if amount < item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    item.amount = item.amount - amount
                    item.save()
                    amount = 0

                elif amount == item.amount :
                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    item.delete()
                    amount = 0
                
                elif amount > item.amount :

                    if Wallet.objects.filter(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency):
                        wal = Wallet.objects.get(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                        wal.amount = wal.amount + amount
                        wal.save()
                    else:
                        wal = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).bcurrency, amount = amount)
                        wal.save()

                    if Wallet.objects.filter(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency):
                        wal2 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).scurrency)
                        wal2.amount = wal2.amount + (amount * item.price)
                        wal2.save()
                    else:
                        wal2 = Wallet(user = item.user , currency = ProTrades.objects.get(id = trade).scurrency, amount = (amount * item.price))
                        wal2.save()
                    wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                    wal3.amount = wal3.amount - amount
                    wal3.save()
                    amount = amount - item.amount
                    item.delete()
                    i = i +1
                    
            if amount > 0 :
                add = ProTradesSellOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price, start = amountstart)
                add.save()
                wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
                wal3.amount = wal3.amount - amount
                wal3.save()
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_201_CREATED)
        else:
            add = ProTradesSellOrder(trade = ProTrades.objects.get(id = trade) ,user = request.user, amount = amount , price = price , start = amountstart)
            add.save()
            wal3 = Wallet.objects.get(user = request.user , currency = ProTrades.objects.get(id = trade).bcurrency)
            wal3.amount = wal3.amount - amount
            wal3.save()
            return Response(status=status.HTTP_201_CREATED)




class protradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, id):
        return ProTrades.objects.get(id = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        if len(ProTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            minsell = ProTradesSellOrder.objects.filter(trade = maintrade).order_by('price')[0].price
        else:
            minsell = 0
        if len(ProTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            maxbuy = ProTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')[0].price
        else:
            maxbuy = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        else:
            sbalance = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        else:
            bbalance = 0
        serializer = {'smin': minsell, 'bmax': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance}
        print(serializer)
        return Response(serializer,status=status.HTTP_201_CREATED)

class protradesselllist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesSellOrder.objects.filter(user = user)

    def get(self , request, format=None):
        if len(self.get_object(request.user)) < 1 :
            return Response(status=status.HTTP_400_BAD_REQUEST)
        userinfo =  self.get_object(request.user)
        serializer = ProTradesSellOrderSerializer(userinfo , many=True)
        return Response(serializer.data)

class protradesbuylist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return ProTradesBuyOrder.objects.filter(user = user)

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ProTradesBuyOrderSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)




class fasttradesinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self ,id):
        return MainTrades.objects.get(id = id)

    def get(self , request, id, format=None):
        maintrade =  self.get_object(id)
        maxsell = 0
        maxbuy = 0
        if len(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price')) > 0:
            for item in MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price'):
                maxsell += item.amount
        if len(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price')) > 0:
            for itemm in MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price'):
                maxbuy += item.amount
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.scurrency))>0):
            sbalance = Wallet.objects.get(user = request.user , currency = maintrade.scurrency).amount
        else:
            sbalance = 0
        if(len(Wallet.objects.filter(user = request.user , currency = maintrade.bcurrency))>0):
            bbalance = Wallet.objects.get(user = request.user , currency = maintrade.bcurrency).amount
        else:
            bbalance = 0        
        buymaintrades = MainTradesBuyOrderSerializer(MainTradesBuyOrder.objects.filter(trade = maintrade).order_by('-price'),many=True)
        sellmaintrades = MainTradesSellOrderSerializer(MainTradesSellOrder.objects.filter(trade = maintrade).order_by('price'),many=True)
        serializer = {'maxsell': maxsell, 'maxbuy': maxbuy, 'sbalance': sbalance, 'bbalance': bbalance, 'buymaintrades': buymaintrades.data,'sellmaintrades': sellmaintrades.data}
        return Response(serializer)

class indexprice(APIView):
    def get(self , request, format=None):
        response = Indexprice.objects.all().reverse()[0].price
        return HttpResponse(response) 

class indexhistory(APIView):
    def get(self , request, format=None):
        r = Indexprice.objects.all().reverse()[0].PriceHistory
        return HttpResponse(r) 

class perpetualrequest(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request, format=None):
        if Perpetual.objects.filter(user = request.user) :
            return HttpResponse(2) 
        if PerpetualRequest.objects.filter(user = request.user) :
            return HttpResponse(1) 
        return HttpResponse(0) 
    def post(self , request, format=None):
        if len(PerpetualRequest.objects.filter(user = request.user)) < 1:
            if len(Perpetual.objects.filter(user = request.user)) < 1:
                per = PerpetualRequest(user = request.user)
                per.save()
        return Response(status=status.HTTP_201_CREATED)
    def put(self , request, format=None):
        if Perpetual.objects.filter(user = request.user) :
            return HttpResponse(True) 
        return HttpResponse(False) 

class buy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.all().order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


    def post(self , request, format=None):
        request.data['user'] = request.user.id
        serializer = BuySerializer(data = request.data)
        if serializer.is_valid():
            wallet = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 1))
            if wallet.amount < float(request.data['ramount']):
                return Response({'error':' موجودی کافی نیست . ابتدا حساب ریالی خود را شارژ نمایید'} )
            wallet.amount = wallet.amount - float(request.data['ramount'])
            wallet.save()
            request.data['user'] = request.user.id
            swal = Cp_Wallet.objects.get(user = request.user,currency = Cp_Currencies.objects.filter(brand = request.data['currency']).last())
            swal.balance = swal.balance + float(request.data['camount'])
            swal.save()
            serializer.save()
            sms(user = User.objects.get(id = 5) ,text= ' درخواست خرید مقدار' + str(request.data['camount']) + 'از ارز' + request.data['currency'] + 'برای ' + request.user.username, pattern= 'tfpvvl8beg')
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class buyout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request, format=None):
        request.data['user'] = request.user.id
        serializer = BuyoutSerializer(data = request.data)
        if serializer.is_valid():
            wallet = Wallet.objects.get(user = request.user , currency = Currencies.objects.get(id = 1))
            if wallet.amount < float(request.data['ramount']):
                return Response({'error':' موجودی کافی نیست . ابتدا حساب ریالی خود را شارژ نمایید'} )
            wallet.amount = wallet.amount - float(request.data['ramount'])
            wallet.save()
            serializer.save()
            sms(user = User.objects.get(id = 5)  ,text= ' درخواست خرید ولت خارجی به مقدار' + str(request.data['camount']) + 'از ارز' + request.data['currency'] + 'برای ' + request.user.username, pattern= 'tfpvvl8beg')
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class buyoutopen(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyoutrequest.objects.filter(user = user , act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuyoutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

        
class buyopen(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.filter(user = user , act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class buyouthis(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyoutrequest.objects.filter(user = user , act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuyoutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class buyhis(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return buyrequest.objects.filter(user = user , act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = BuySerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sellout(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]


    def post(self , request, format=None):
        request.data['user'] = request.user.id
        serializer = selloutSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            sms(user = User.objects.get(id = 5) ,text= ' درخواست فروش ولت خارجی به مقدار' + str(request.data['camount']) + 'از ارز' + request.data['currency'] + 'برای ' + request.user.username, pattern= 'r4hxan3byx')
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

class selloutopen(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return selloutrequest.objects.filter(user = user , act = 0).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = selloutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sellouthis(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return selloutrequest.objects.filter(user = user , act = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = selloutSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sellhis(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return sellrequest.objects.filter(user = user , act__gte = 2).order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = SellSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

class sell(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request, format=None):
        request.data['user'] = request.user.id
        if not len(Cp_Wallet.objects.filter(user = request.user, currency = Cp_Currencies.objects.filter(brand = request.data['currency']).last())):
            return Response({'error':'موجودی کافی نیست'} )
        swal = Cp_Wallet.objects.get(user = request.user, currency = Cp_Currencies.objects.filter(brand = request.data['currency']).last())
        balance = swal.balance
        if float(balance) < float(request.data['camount']):
            return Response({'error':'موجودی کافی نیست'} )
        swal.balance = swal.balance - float(request.data['camount'])
        swal.save()
        wal = Wallet.objects.get(user = request.user, currency = Currencies.objects.get(id = 1))
        wal.amount = wal.amount + request.data['ramount']
        wal.save()
        serializer = SellSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
        note = Notification(user=request.user, title = 'فروش موفق' , text = ' درخواست فروش شما با موفقیت انجام شد . ')
        note.save()
        return Response(status=status.HTTP_201_CREATED)


class exchange(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get_object(self, user):
        return exchangerequest.objects.all().order_by('-date')

    def get(self , request, format=None):
        maintrade =  self.get_object(request.user)
        serializer = ExchangeSerializer(maintrade , many=True)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


    def post(self , request, format=None):
        request.data['user'] = request.user.id
        serializer = ExchangeSerializer(data = request.data)
        if serializer.is_valid():
            if not len(Cp_Wallet.objects.filter(currency = Cp_Currencies.objects.filter(brand = request.data['currency']).last(), user = request.user)):
                return Response({'error':'موجودی کافی نیست'} )
            swal = Cp_Wallet.objects.get(currency = Cp_Currencies.objects.filter(brand = request.data['currency']).last(), user = request.user)
            balance = swal.balance
            if float(balance) < float(request.data['camount']):
                return Response({'error':'موجودی کافی نیست'} )
            swal.balance = swal.balance - float(request.data['camount'])
            swal.save()
            note = Notification(user=request.user, title = 'فروش موفق' , text = ' درخواست فروش شما با موفقیت انجام شد . ')
            note.save()
            if not len(Cp_Wallet.objects.filter(currency = Cp_Currencies.objects.filter(brand = request.data['currency2']).last(), user = request.user)):
                bwal = Cp_Wallet(currency = Cp_Currencies.objects.filter(brand = request.data['currency2']).last(), user = request.user, balance = float(request.data['camount2']))
                bwal.save()
            else:
                bwal = Cp_Wallet.objects.get(currency = Cp_Currencies.objects.filter(brand = request.data['currency2']).last(), user = request.user)
                bwal.balance = bwal.balance + float(request.data['camount2'])
                bwal.save()
            serializer.save()
            try:
                sms(user = User.objects.get(id = 5) ,text= ' درخواست تبدیل مقدار' + str(request.data['camount']) + 'از ارز' + request.data['currency'] + 'برای ' + request.user.username, pattern= 'tfpvvl8beg')
                sms(user = User.objects.get(id = 1) ,text= ' درخواست تبدیل مقدار' + str(request.data['camount']) + 'از ارز' + request.data['currency'] + 'برای ' + request.user.username, pattern= 'tfpvvl8beg')
            except:
                pass
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

# < ------------   Margin Trades 


class oltradeinfo(APIView):


    def get(self , request, format=None):   
        list = {} 
        r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
        list = r.json()['data']['ticker']
        list2 = {}
        for item in Leverage.objects.all():
            if item.symbol in list:
                list2[item.symbol] = list[item.symbol]
        return Response(list2)

class oltradeinfo3(APIView):


    def get(self , request, format=None):   
        price = Price.objects.get()
        rial = price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent / 100))
        list = {}
        r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
        list = r.json()['data']['ticker']
        list2 = {}
        for item in Leverage.objects.all():
            if item.symbol == 'BTCUSDT':
                list2[item.symbol] = list[item.symbol]
                pprice = float(list[item.symbol]['last'])
                list2[item.symbol]['last'] = pprice 
                list2[item.symbol]['change'] = (float(list[item.symbol]['last']) - float(list[item.symbol]['open'])) / float(list[item.symbol]['open']) * 100
                list2[item.symbol]['rial'] = pprice * (price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent3 / 100)))
            elif 'USDT' in item.symbol:
                if item.symbol in list:
                    list2[item.symbol] = list[item.symbol]
                    pprice = float(list[item.symbol]['last'])
                    list2[item.symbol]['last'] = pprice 
                    list2[item.symbol]['change'] = (float(list[item.symbol]['last']) - float(list[item.symbol]['open'])) / float(list[item.symbol]['open']) * 100
                    list2[item.symbol]['rial'] = pprice * rial
        return Response(list2)

class oltradeinfo4(APIView):


    def get(self , request, format=None):   
        query = Leverage.objects.all().order_by('-last')
        serializer = Oltrade4Serializer(query, many=True)
        return Response(serializer.data)


class olboardinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.market_depth(access_id=Perpetual.objects.get(user=request.user).apikey,market = request.data['sym'],tonce=time.time()*1000,))
        
class cp_balance(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_account(market =  request.data['sym']))
    

class cp_borrow(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_loan(market =  request.data['market'],amount = request.data['amount'],coin_type=request.data['coin']))
    
class cp_borrow_get(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_loan_get(account_id =  request.data['mid']))
            
class cp_repay(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_flat(market =  request.data['market'],amount = request.data['amount'],coin_type=request.data['coin']))
        

class cp_borrowlist(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_loan_history(market =  request.data['market']))
  

class cp_ticker(APIView):
    def post(self , request, format=None):
        price = Price.objects.get()
        rial = price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent / 100))
        if request.data['sym'] == 'BTC':
            rial = price.usd + (price.usd * (General.objects.get(id = 1).USDTpercent3 / 100))
        if request.data['sym'] == 'USDT':
            r = requests.get(url = 'https://api.coinex.com/v1/common/currency/rate')
            r = r.json()['data']['USDT_to_USD']
            print(r)
            price = float(r) + (float(r) * General.objects.get(id =1).USDTpercent2 / 100)
            return Response({'buy' : price, 'last' : price, 'rial': price * rial})
        r2 = requests.get(url = 'https://api.coinex.com/v1/common/currency/rate')
        r2 = r2.json()['data']['USDT_to_USD']
        r2 = (float(r2) + (float(r2) * General.objects.get(id =1).USDTpercent2 / 100))
        list = {} 
        r = requests.get(url = 'https://api.coinex.com/v1/market/ticker/all')
        list = r.json()['data']['ticker']
        price = float(list[request.data['sym']+'USDT']['last']) 
        list = {}
        list['last'] = price
        list['buy'] = price
        list['rial'] = price * rial
        return Response(list)
        

class cp_address(APIView):
    def post(self , request, format=None):
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7' )
        return Response(coinex.balance_deposit_address(coin_type =  request.data['sym']))

class cp_mg_transfer(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_transfer(from_account=0, to_account=27, coin_type='USDT', amount='23'))

class cp_pending(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_pending(market =  request.data['sym'],account_id=request.data['mid']))

class cp_stop_pending(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_stop_pending(market =  request.data['sym'],account_id=request.data['mid']))


class cp_close(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.close_market(
            request.data['market'],
            request.data['id']
        )
        return HttpResponse(json.dumps(result, indent=4))

class cp_finished(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_finished(market = request.data['sym'],account_id=request.data['mid']))


class cp_stop_finished(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_stop_finished(market = request.data['sym'],account_id=request.data['mid']))

class cp_transfer(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.margin_transfer(from_account=int(request.data['fa']), to_account=int(request.data['ta']), coin_type=request.data['coin'] , amount=str(request.data['amount'])))

class cp_market_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_market(account_id=request.data['mid'],access_id=Perpetual.objects.get(user=request.user).apikey,market = request.data['market'],type=request.data['type'],amount=request.data['amount'],tonce=time.time()*1000,))
        

class cp_limit_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_limit(account_id=request.data['mid'],access_id=Perpetual.objects.get(user=request.user).apikey,market = request.data['market'],type=request.data['type'],amount=request.data['amount'],price=request.data['price'],tonce=time.time()*1000,))


class cp_stop_limit_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_stop_limit(account_id=request.data['mid'],access_id=Perpetual.objects.get(user=request.user).apikey,market = request.data['market'],type=request.data['type'],amount=request.data['amount'],price=request.data['price'],stop_price=request.data['stop_price'],tonce=time.time()*1000,))



class cp_cancel_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_pending_cancel(market = request.data['market'],id = request.data['id']))
        
class cp_stop_cancel_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.order_stop_pending_cancel( market = request.data['market'],id = request.data['id']))
        
class cp_mg_market(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request):
        r = requests.get('https://api.coinex.com/v1/margin/market')
        r = r.json()
        result = []
        for item in r['data'] :
            if 'USDT' in item :
                result.append([item, r['data'][item]])
        return Response(result)

class cp_mg_usdt(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request):
        usdt = Wallet.objects.filter( Q(user = request.user, currency = Currencies.objects.get(id = 4)) | Q(user = request.user, currency = Currencies.objects.get(id = 41)))
        serializer = WalletSerializer(usdt , many = True)
        return Response(serializer.data)


class cp_mg_main(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        return Response(coinex.balance_info())

    def post(self , request):
        wal = Cp_Wallet.objects.filter(user= request.user, currency = Cp_Currencies.objects.filter(brand = request.data['sym']).last())
        if(len(wal)):
            wal = wal.last().balance
        else:
            wal = 0
        return Response(wal)

class cp_mg_settings(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        print(coinex.balance_deposit_address('TRX'))
        return HttpResponse(coinex.balance_deposit_address('TRX'))


class cp_withdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self, request, id , format=None):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        brand = Cp_Currencies.objects.get(name = id).brand
        chain = id.replace(brand , '').replace('-' , '')
        amount = request.data['amount']
        address = request.data['address']
        res = coinex.sub_account_transfer(coin_type=brand,amount=amount)
        print(res)
        if not res:
            withdraw = Cp_Withdraw(user = request.user , currency = Cp_Currencies.objects.get(name = id) , amount = amount , chain = chain , address = address)
            withdraw.save()
            return Response(res)
        return Response(res)

class withdraw(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self, request , format=None):
        request.data['user'] = request.user.id
        serializer = WithdrawSerializer(data = request.data)
        if serializer.is_valid():
            wa = Wallet.objects.get(user= request.user , currency=1)
            if int(request.data['amount']) > wa.amount :
                return Response('موجودی کافی نیست', status=status.HTTP_400_BAD_REQUEST)
            else:
                wa.amount = wa.amount - int(request.data['amount'])
                wa.save()
                serializer.save()
                return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class cp_deposit(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self, request , format=None):
        request.data['user'] = request.user.id
        serializer = CpDepositRequestSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        
class cp_wallets(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        result = {}
        for item in Cp_Currencies.objects.all():
            if len(Cp_Wallet.objects.filter(currency = item , user= request.user)):
                wal = Cp_Wallet.objects.get(currency = item , user= request.user)
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':wal.balance}
            else: 
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':'0'}
        return Response(result)

    def post(self , request , format=None):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        res = coinex.balance_info()
        return Response(res)

class cp_wallets2(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        result = {}
        for item in Cp_Currencies.objects.all():
            if item.brand != 'USDT':
                if len(Cp_Wallet.objects.filter(currency = item , user= request.user)):
                    wal = Cp_Wallet.objects.get(currency = item , user= request.user)
                    result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':wal.balance}
                else: 
                    result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':'0'}
        return Response(result)

    def post(self , request , format=None):
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        res = coinex.balance_info()
        return Response(res)


class cp_wallet(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get_object(self , user , id):
        try:
            return Cp_Wallet.objects.filter(user = user , currency = id)
        except Wallet.DoesNotExist:
            return False
    
    def get(self, request, id , format=None):
        item = Cp_Currencies.objects.get(name = id)
        brand = item.brand
        curs = Cp_Currencies.objects.filter(brand = brand)
        for item in curs:
            result = {}
            if len(Cp_Wallet.objects.filter(currency = item , user= request.user)):
                wal = Cp_Wallet.objects.get(currency = item , user= request.user)
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':wal.balance}
            else: 
                result[item.brand] = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':'0'}
        return Response(result)

    def post(self , request, id, format=None):   
        brand = id
        curs = Cp_Currencies.objects.filter(brand = brand)
        wallets = {}
        for item in curs:
            wallets[item.name] = ''
        coinex = CoinEx(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey )
        res = coinex.balance_info()
        result = {}
        if brand in res.keys() :
            result = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':res[item.brand],'address' : wallets}
        else: 
            result = {'name' : item.name ,  'brand' : item.brand,'chain' : item.chain,'can_deposit' : item.can_deposit,'can_withdraw' : item.can_withdraw,'deposit_least_amount' : item.deposit_least_amount,'withdraw_least_amount' : item.withdraw_least_amount,'withdraw_tx_fee' : item.withdraw_tx_fee,'balance':'0','address' : wallets}
        return Response(result)

class cp_history(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, id , format=None):
        if id == 'false':
            coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')
            res = coinex.sub_account_transfer_history(sub_user_name= Perpetual.objects.get(user=request.user).name)
            return Response(res)
        brand = Cp_Currencies.objects.get(name = id).brand
        coinex = CoinEx('56255CA42286443EB7D3F6DB44633C25', '30C28552C5B3337B5FC0CA16F2C50C4988D47EA67D03C5B7')
        res = coinex.sub_account_transfer_history(sub_user_name= Perpetual.objects.get(user=request.user).name, coin_type=brand)
        print(res)
        return Response(res)

class cp_currency(APIView):
    
    def get(self , request ,id):
        userinfo = Cp_Currencies.objects.filter(name = id)
        serializer = CpCurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)

class cp_currencies(APIView):

    def get(self , request):
        userinfo = Cp_Currencies.objects.all().order_by('id')
        serializer = CpCurrenciesSerializer(userinfo , many=True)
        return Response(serializer.data)

#  Margin Trades ------------ >


#  < ------------ Perpetual Trades 



class olptradeinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = {}
        tick = robot.tickers()
        for key in tick['data']['ticker']:
            if not '_' in key and 'USDT' in key :
                result[f'{key}'] = tick['data']['ticker'][key]['last']
        return Response(result)

class olpboardinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.depth(market = request.data['sym'])
        return Response(result)

class olpmarketinfo(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def get(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.get_market_info()
        return Response(result)

class cpp_adjustleverage(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.adjust_leverage(position_type=2, market= request.data['sym'], leverage= request.data['leverage'])
        return Response(result)

class cpp_balance(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.query_account()
        return Response(result)

class cpp_pending(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.query_order_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpp_stop_pending(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.query_stop_pending(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpp_close(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.close_market(
            request.data['sym'],
            request.data['id']
        )
        return HttpResponse(json.dumps(result, indent=4))

class cpp_finished(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.query_order_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)

class cpp_stop_finished(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request, format=None):   
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.query_stop_finished(market=request.data['sym'], side = 0, offset=False)
        return Response(result)


class cpp_market_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.put_market_order(market=request.data['sym'], amount= request.data['amount'], side=request.data['type'])
        return Response(result)


class cpp_limit_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.put_limit_order(market = request.data['sym'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'])
        return Response(result)


class cpp_stop_limit_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.put_stop_limit_order(market = request.data['sym'],side=request.data['type'],amount=request.data['amount'],price=request.data['price'],stop_price=request.data['stop_price'])
        return Response(result)



class cpp_cancel_order(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    def post(self , request):
        robot = CoinexPerpetualApi(Perpetual.objects.get(user=request.user).apikey, Perpetual.objects.get(user=request.user).secretkey)

        result = robot.close_market(market = request.data['sym'],id = request.data['id'])
        return Response(result)


class topsticker(APIView):
    def get():
        query = TopSticker.objects.all()
        serializer = TopStickerSerializer(query , many =True)
        return Response(serializer.data)

class bottomsticker(APIView):
    def get():
        query = BottomSticker.objects.all()
        serializer = BottomStickerSerializer(query , many =True)
        return Response(serializer.data)

class posts(APIView):
    def get(self , request , format=None):
        query = Posts.objects.all()
        serializer = PostsSerializer(query , many =True)
        return Response(serializer.data)

class news(APIView):
    def get():
        query = News.objects.all()
        serializer = NewsSerializer(query , many =True)
        return Response(serializer.data)




class topsticker(APIView):
    def get(self , request , format=None):
        pages = TopSticker.objects.all()
        serializer = TopStickerSerializer(pages , many=True)
        return Response(serializer.data)

    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class bottomsticker(APIView):
    def get(self , request , format=None):
        pages = BottomSticker.objects.all().order_by('id')
        serializer = BottomStickerSerializer(pages , many=True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class mainpageposts(APIView):
    def get(self , request , format=None):
        query = Posts.objects.all().order_by('-id')[:3]
        serializer = PostsSerializer(query , many =True)
        return Response(serializer.data)
        
    def post(self , request , format=None):
        serializer = PagesSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self , request , format=None):
        pages = Pages.objects.filter(position = 'others', name=request.data['name'])
        serializer = PagesSerializer(pages , many=True)
        return Response(serializer.data)

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

    def delete(self , request , format=None):
        serializer = Pages.objects.get(id=request.data['id'])
        serializer.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def review(request):
    rev = Review()
    rev.save()
    return HttpResponse()

class levelfee(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = LevelFee.objects.filter(id = UserInfo.objects.get(user = request.user).level)
        serializer = LevelFeeSerializer(user , many=True)
        return Response(serializer.data)
        
class generalbtc(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response(General.objects.get().USDTpercent3)
    
class sellpercent(APIView):
    
    def get(self, request, *args, **kwargs):
        return Response(General.objects.get().sellpercent)


class alert(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        query = Alert.objects.filter(page = request.data['page'])
        if not len(query):
            return Response ('')
        serializer = AlertSerializer(query.last())
        return Response(serializer.data)


class p2prequests(GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    queryset = P2pRequest.objects.filter(status__lt = 10)
    serializer_class = P2pRequestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get(self , request , format=None):
        return self.list(request)

    def post(self , request , format=None):
        return self.create(request , user = request.user)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self , request, pk):
        a = P2pRequest.objects.get(rid = pk)
        a.status = 10
        a.save()
        return self.list(request)
    

class p2pmyorders(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]


    def get(self , request , format=None):
        query = P2pRequest.objects.filter(user = request.user, status__lt = 10)
        serializer = P2pRequestSerializer(query , many=True)
        return Response(serializer.data)

    def post(self , request, id, format=None):
        query = P2pRequest.objects.get(rid=id)
        serializer = P2pRequestSerializer(query)
        return Response(serializer.data)

class p2pmybuyorders(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]


    def get(self , request , format=None):
        query = P2pBuyRequest.objects.filter(Q(user = request.user) | Q(user2 = request.user) , status__lt = 9)
        serializer = P2pBuyRequestSerializer(query , many=True)
        return Response(serializer.data)




class p2pbuy(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)

    def post(self , request, id):
        req = P2pBuyRequest.objects.create(user = request.user, amount = float(request.data['amount']), request = P2pRequest.objects.get(rid = id), user2 = P2pRequest.objects.get(rid = id).user)
        return Response(req.rid)

    def put(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        req.wallet = request.data['wallet']
        req.memo = request.data['memo']
        req.details = request.data['details']
        req.save()
        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)

    def delete(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        req.status = 10
        req.save()
        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)


class p2pbuyaccept(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        req.status = 1
        req.save()
        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)

class p2psent(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        req.status = 3
        req.save()
        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)



class p2pacceptget(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def post(self , request, id):
        req = P2pBuyRequest.objects.get(rid = id)
        req.status = 4
        req.save()
        user = req.user2
        wal =Wallet.objects.filter(user=user , currency = Currencies.objects.get())
        if not req.request.done:
            req.request.done = req.amount
            req.request.save()
        else:
            req.request.done = float(req.request.done) + req.amount
            req.request.save()
        if req.request.done == req.request.balance:
            req.request.status = 2
        if len(wal):
            wal= wal.last()
            wal.amount = wal.amount + (req.request.price * req.amount)
            wal.save()
        else:
            wal = Wallet.objects.create(user=user , currency = Currencies.objects.get())
            wal.amount = wal.amount + (req.request.price * req.amount)
            wal.save()

        serializer = P2pBuyRequestSerializer(req)
        return Response(serializer.data)


P2PCallbackURL = 'https://amizax.com/api/v1/p2pverifys/'


class p2pbuypay(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def to_bank(self, rid , req, request):
        
        amount = int((req.request.price * req.amount))/10
        uid = str(rid)
        
        payload='api_key=5a273bf9-c01e-48bd-abd2-816563ad61cc&amount=' +str(amount)+ '&order_id=&customer_phone=&callback_uri=' + P2PCallbackURL 
        headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
        }
        trans = requests.request("POST", NP_API_REQUEST, headers=headers, data=payload).json()
        tr = Transactionid(user = request.user , transid = uid , amount = (req.request.price * req.amount), tid = trans['trans_id'])
        tr.save()
        return Response(f"{trans}")


    def post(self , request, id):
        if not SmsCode.objects.filter(user = request.user, number = request.data['code'], date__gt = datetime.now() - timedelta(minutes=20)):
            return Response(status=status.HTTP_403_FORBIDDEN)
        req = P2pBuyRequest.objects.get(rid = id)
        if len(Wallet.objects.filter(user=request.user, currency = Currencies.objects.get())):
            wal = Wallet.objects.get(user=request.user, currency = Currencies.objects.get())
            if wal.amount >= (req.request.price * req.amount):
                wal.amount = wal.amount - (req.request.price * req.amount)
                wal.save()
                req.status = 2
                req.save()
                serializer = P2pBuyRequestSerializer(req)
                return Response(serializer.data)
            else:
                return self.to_bank(id, req, request)
        else:
            return self.to_bank(id, req, request)
        

def p2pverifys(request):
    tid = request.GET.get('trans_id', '')
    transactioni = Transactionid.objects.get(tid = tid)
    req = P2pBuyRequest.objects.get(rid = transactioni.transid)
    amount = request.GET.get('amount', '')
    payload='api_key=5a273bf9-c01e-48bd-abd2-816563ad61cc&amount='+str(amount)+ f'&trans_id={tid}'
    headers = {
    'User-Agent': 'PostmanRuntime/7.26.8',
    'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", NP_API_VERIFY, headers=headers, data=payload).json()
    if int(response['code']) == 0:
        if amount == (req.request.price * req.amount):
            req.status = 2
            req.save()
            return redirect(f'https://amizax.com/p2psuccess/{req.rid}')
        else:
            wal = Wallet.objects.get(user=request.user, currency = Currencies.objects.get())
            if wal.amount >= ((req.request.price * req.amount) - amount):
                wal.amount = wal.amount - ((req.request.price * req.amount) - amount)
                wal.save()
                req.status = 2
                req.save()
                return redirect(f'https://amizax.com/p2psuccess/{req.rid}')
    else:
        return render(request, 'failure.html', {'message': 'خطایی رخ داده است'})



class chains(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = Cp_Currencies.objects.filter(brand = request.data['brand'])
        serializer = ChainSerializer(user , many=True)
        return Response(serializer.data)


class MyChatRooms(GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self , request , format=None):
        queryset = ChatRoom.objects.filter(Q(user1=request.user) | Q(user2=request.user))
        serializer = ChatRoomSerializer(queryset, many=True)
        return Response(serializer.data)


class ChatTexts(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication, authentication.TokenAuthentication ]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        if User.objects.get(username=id) == request.user:
            return Response(False)
        queryset = ChatText.objects.filter(room = ChatRoom.objects.get(Q(user1=request.user , user2=User.objects.get(username=id)) | Q(user2=request.user, user1=User.objects.get(username=id)))).order_by('id')
        serializer = ChatTextSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self , request, id):
        if User.objects.get(username=id) == request.user:
            return Response([])
        if len(ChatRoom.objects.filter(user1 = request.user, user2 = User.objects.get(username= id))):
            chatroom = ChatRoom.objects.get(user1 = request.user, user2 = User.objects.get(username= id))
            textchat = ChatText.objects.create(user = request.user, room = chatroom, text = request.data['text'])
            textchat.save()
        elif len(ChatRoom.objects.filter(user2 = request.user, user1 = User.objects.get(username= id))):
            chatroom = ChatRoom.objects.get(user2 = request.user, user1 = User.objects.get(username= id))
            textchat = ChatText.objects.create(user = request.user, room = chatroom, text = request.data['text'])
            textchat.save()
        else:
            chatroom = ChatRoom.create(user1 = request.user, user2 = User.objects.get(username= id))
            textchat = ChatText.objects.create(user = request.user, room = chatroom, text = request.data['text'])
            textchat.save()
        query = ChatText.objects.filter(room = chatroom)
        serializer = ChatTextSerializer(query, many = True)
        return Response(serializer.data)