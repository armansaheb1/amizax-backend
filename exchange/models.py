from typing import Text
from django.db import models
from io import BytesIO
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.query_utils import select_related_descend
from django.utils import timezone
import uuid
from django.core.files import File
from django.utils.translation import deactivate
from requests.api import post
from jsonfield import JSONField
from datetime import date, datetime    
import django
from sarafi.settings import ROOT, SECRET_KEY
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.utils.timezone import utc
import pyotp
import base32_lib

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = f"{ROOT}" + "/resetpass/{}".format(reset_password_token.key)

    send_mail(
        # title:
        "برای تغییر کلمه عبور خود از لینک زیر استفاده کنید",
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class transactionid(models.Model):
    user = models.ForeignKey(User , related_name='transactionid', on_delete=models.CASCADE)
    transid = models.UUIDField(editable=False)
    amount = models.BigIntegerField(null=True)

class Referal(models.Model):
    inviting = models.ForeignKey(User , related_name='referals' , on_delete=models.CASCADE)
    inviter = models.IntegerField()


class UserInfo(models.Model):
    user = models.OneToOneField(User , related_name='userinfo', on_delete=models.CASCADE)
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    mobile = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,null=True)
    email = models.EmailField()
    address = models.CharField(max_length=500, null=True)
    post = models.CharField(max_length=10, null=True)
    level = models.IntegerField(default= 0)
    is_active = models.BooleanField(default=True)
    is_verify = models.BooleanField(default=False)
    smsverify = models.BooleanField(default=False)
    googleverify = models.BooleanField(default=False)
    emailverify = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    last_visit = models.DateTimeField(default=timezone.now)
    complete = models.BooleanField(default=False)
    otp = models.CharField(max_length=100 ,default= base32_lib.generate(length=16, checksum=True))
    referalid = models.UUIDField(default=uuid.uuid4 , null=False)
    class meta:
        ordering = ('-date_joined',)
        
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return f'/{self.username}/'

    def get_otp(self):
        return f'otpauth://totp/admin?secret={self.otp}&algorithm=SHA1&digits=6&period=30'

    def get_melli(self):
        if len(VerifyMelliRequest.objects.filter(user= self.user)):
            return VerifyMelliRequest.objects.get(user= self.user).mellic
        else:
            return ''
    def get_mellip(self):
        if len(VerifyMelliRequest.objects.filter(user= self.user)):
            return f'{ROOT}/media/{VerifyMelliRequest.objects.get(user= self.user).melliimg}'
        else:
            return ''
    def is_staff(self):
        return self.user.is_staff

    def get_referal(self):
        return 'https://www.amizax.com/register/' + str(self.referalid)


class SmsVerified(models.Model):
    number = models.CharField(max_length=20)
    date = models.DateTimeField(default=datetime.now())

class LevelFee(models.Model):
    id = models.IntegerField(primary_key=True)
    buy = models.FloatField(default=0)
    sell = models.FloatField(default=0)
    perpetual = models.FloatField(default=0)
    margin = models.FloatField(default=0)
    exchange = models.FloatField(default=0)


class Review(models.Model):
    date = models.DateTimeField(default=timezone.now)

class General(models.Model):
    name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    mobile= models.CharField(max_length=255)
    whatsapp= models.CharField(max_length=255)
    telegram= models.CharField(max_length=255)
    instagram= models.CharField(max_length=255)
    telephone= models.CharField(max_length=255)
    rule = models.CharField(max_length=1000000 , null=True)
    logo = models.ImageField(upload_to='general' , null = True)
    USDTpercent = models.FloatField(null=True)
    USDTpercent2 = models.FloatField(null=True)


class mobilecodes(models.Model):
    number = models.CharField(max_length=15)
    code = models.CharField(max_length=15)
    def __str__(self):
        return self.number

class buyrequest(models.Model):
    user = models.ForeignKey(User , related_name='buys' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=20)
    ramount = models.BigIntegerField()
    rramount = models.FloatField(null=True)
    camount = models.FloatField()
    act = models.IntegerField(default=0 )
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class buyapp(models.Model):
    user = models.ForeignKey(User , related_name='buyapps' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    type = models.IntegerField()
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class sellrequest(models.Model):
    user = models.ForeignKey(User , related_name='sells' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=20)
    ramount = models.FloatField()
    camount = models.FloatField()
    act = models.IntegerField(default=2)
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class exchangerequest(models.Model):
    user = models.ForeignKey(User , related_name='exchanges' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=20)
    currency2 = models.CharField(max_length=20)
    camount = models.FloatField()
    camount2 = models.FloatField()
    act = models.IntegerField(default=0)
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class buyoutrequest(models.Model):
    user = models.ForeignKey(User , related_name='buyout' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    ramount = models.BigIntegerField()
    rramount = models.FloatField(null=True)
    camount = models.FloatField()
    act = models.IntegerField(default=0)
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class selloutrequest(models.Model):
    user = models.ForeignKey(User , related_name='sellout' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    currency = models.CharField(max_length=20)
    hash = models.CharField(max_length=200)
    ramount = models.FloatField()
    rramount = models.FloatField(null=True)
    camount = models.FloatField()
    act = models.IntegerField(default=0)
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class Perpetual(models.Model):
    user = models.ForeignKey(User , related_name='Perpetual' , on_delete=models.CASCADE , null=True,)
    name = models.CharField(max_length=255, null=True)
    secretkey = models.CharField(max_length=255)
    apikey = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.user.username}'


class PerpetualRequest(models.Model):
    user = models.ForeignKey(User , related_name='Perpetualreq' , on_delete=models.CASCADE , null=True,)
    date = models.DateTimeField(default=timezone.now)

    def get_user(self):
        return self.user.username
        
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class Indexprice(models.Model):
    price = JSONField()
    PriceHistory = JSONField()

class Staff(models.Model):
    user = models.ForeignKey(User , related_name='staffs' , on_delete=models.CASCADE)
    level = models.IntegerField()

class Currencies(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    pic = models.ImageField(upload_to='cur' , null = True)
    class Meta:
        verbose_name = ' ارز '
        verbose_name_plural = ' ارز ها'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'currencies/{self.name}/'
    def get_image(self):
        return f'{ROOT}/media/{self.pic}'

class Wallet(models.Model):
    user = models.ForeignKey(User  , on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies , on_delete=models.CASCADE ,default=0)
    amount = models.FloatField(default=0)
    address = models.CharField(max_length=1000 , null = True, blank=True)
    key = models.CharField(max_length=1000 , null = True ,blank=True)
    accid = models.CharField(max_length=100 , null = True ,blank=True)
    def __str__(self):
        return self.user.username + '--' + self.currency.name
    class Meta:
        verbose_name = ' کیف پول '
        verbose_name_plural = ' کیف پول ها'
    
    def get_currency(self) :
        return f'{self.currency.name}'


class Cp_Currencies(models.Model):
    name = models.CharField(max_length=100 ,)
    brand = models.CharField(max_length=100 ,null=True,)
    chain = models.CharField(max_length=100 ,null=True,)
    can_deposit = models.CharField(max_length=100 ,null=True,)
    can_withdraw = models.CharField(max_length=100 ,null=True,)
    deposit_least_amount = models.CharField(max_length=100 ,null=True,)
    withdraw_least_amount = models.CharField(max_length=100 ,null=True,)
    withdraw_tx_fee = models.CharField(max_length=100 ,null=True,)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'currencies/{self.name}/'
    def get_image(self):
        return f'{ROOT}/media/{self.pic}'

class Cp_Wallet(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    currency = models.ForeignKey(Cp_Currencies , on_delete=models.CASCADE ,default=0)
    balance = models.FloatField()
    
    def get_currency(self) :
        return f'{self.currency.name}'

class Cp_Withdraw(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    currency = models.ForeignKey(Cp_Currencies , on_delete=models.CASCADE ,default=0)
    chain = models.CharField(max_length=10)
    amount = models.FloatField()
    address = models.CharField(max_length=1000 , null = True, blank=True)
    rejected= models.BooleanField(default=False)
    completed= models.BooleanField(default=False)
    
    def get_user(self):
        return self.user.username

    def get_currency(self) :
        return f'{self.currency.name}'
    
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class Verify(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    mobilev = models.BooleanField(default = False , null = True)
    mobilec = models.IntegerField(null = True,default=0)
    emailv = models.BooleanField(default = False , null = True)
    emailc = models.IntegerField(null = True ,default=0)
    acceptv = models.BooleanField(default = False , null = True)
    melliv = models.BooleanField(default = False , null = True)
    bankv = models.BooleanField(default = False , null = True)
    accountv = models.BooleanField(default = False , null = True)
    idv = models.BooleanField(default = False , null = True)
    rulev = models.BooleanField(default = False , null = True)
    coinv = models.BooleanField(default = False , null = True)

    def __str__(self):
        return self.user.username + '--' + UserInfo.objects.get(user=self.user).first_name + ' ' + UserInfo.objects.get(user=self.user).last_name

    def get_melliphoto(self):
        if len(VerifyMelliRequest.objects.filter(user = self.user)) > 0:
            return VerifyMelliRequest.objects.get(user = self.user).get_image()
        else:
            return ''

    def get_acceptphoto(self):
        if len(VerifyAcceptRequest.objects.filter(user = self.user)) > 0:
            return VerifyAcceptRequest.objects.get(user = self.user).get_image()
        else:
            return ''

    def isphone(self):
        if UserInfo.objects.get(user = self.user).phone:
            return True
        else:
            return False

    class meta:
        verbose_name = ' تاییدیه '
        verbose_name_plural = ' تاییدیه ها'


class BankCards(models.Model):
    user =  models.ForeignKey(User , related_name='cards' , on_delete=models.CASCADE)
    number = models.CharField(max_length=16 , null=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username + '--' + self.number
    class meta:
        verbose_name = ' کارت بانک '
        verbose_name_plural = ' کارت های بانک'

class BankAccounts(models.Model):
    user =  models.ForeignKey(User , related_name='accounts' , on_delete=models.CASCADE)
    number = models.CharField(max_length=16 , null=True , blank=True)
    shebac = models.CharField(max_length=50 , null=True)
    status = models.BooleanField(default=False)
    class meta:
        verbose_name = ' حساب بانکی '
        verbose_name_plural = ' حساب های بانک'

class WithdrawRequest(models.Model):
    user = models.ForeignKey(User , related_name='withdraws' , on_delete=models.CASCADE)
    bankaccount = models.ForeignKey(BankAccounts , related_name='account' , on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    amount = models.BigIntegerField()
    act = models.IntegerField(default=0)
    def get_user(self):
        return self.user.username
    def get_sheba(self):
        return self.bankaccount.shebac
    def get_number(self):
        return self.bankaccount.shebac
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class CpDepositRequest(models.Model):
    user = models.ForeignKey(User , related_name='cpdeposits' , on_delete=models.CASCADE)
    hash = models.CharField(max_length=1000)
    currency = models.CharField(max_length=10)
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    act = models.IntegerField(default=0)
    def get_user(self):
        return self.user.username
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes

class VerifyMelliRequest(models.Model):
    user = models.ForeignKey(User , related_name='melli' , on_delete=models.CASCADE)
    melliimg = models.ImageField(upload_to='melli' , null = True)
    mellic = models.CharField(max_length=16 , null=True)
    action = models.BooleanField(default = False)
    def __str__(self):
        return self.user.username 

    class meta:
        verbose_name = ' درخواست تایید کارت ملی '
        verbose_name_plural = ' درخواست های تایید کارت ملی '
    def get_image(self):
        return f'{ROOT}/media/{self.melliimg}'
    def get_user(self):
        user = UserInfo.objects.get(user = self.user)
        return user.first_name + ' ' + user.last_name
    def get_user_id(self):
        return self.user.id

class VerifyAcceptRequest(models.Model):
    user = models.ForeignKey(User , related_name='accept' , on_delete=models.CASCADE)
    acceptimg = models.ImageField(upload_to='accept')
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت ملی '
        verbose_name_plural = ' درخواست های تایید کارت ملی '

    def get_image(self):
        return f'{ROOT}/media/{self.acceptimg}'

    def get_user_id(self):
        return self.user.id
    def get_user(self):
        user = UserInfo.objects.get(user = self.user)
        return user.first_name + ' ' + user.last_name

class VerifyBankRequest(models.Model):
    user = models.ForeignKey(User , related_name='Banks' , on_delete=models.CASCADE)
    bankc = models.CharField(max_length=16 , null=True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید کارت بانکی '
        verbose_name_plural = ' درخواست های تایید کارت بانکی '
    def get_user(self):
        return f'{self.user.username}'
    def get_first(self):
        return f'{UserInfo.objects.get(user=self.user).first_name}'
    def get_last(self):
        return f'{UserInfo.objects.get(user=self.user).last_name}'

class VerifyBankAccountsRequest(models.Model):
    user = models.ForeignKey(User , related_name='BanksAccounts' , on_delete=models.CASCADE)
    bankc = models.CharField(max_length=16 , null=True , blank=True)
    shebac = models.CharField(max_length=50 , null=True)
    action = models.BooleanField(default = False)
    class meta:
        verbose_name = ' درخواست تایید حساب بانکی '
        verbose_name_plural = ' درخواست های تایید حساب بانکی '
    def get_user(self):
        return f'{self.user.username}'
    def get_first(self):
        return f'{UserInfo.objects.get(user=self.user).first_name}'
    def get_last(self):
        return f'{UserInfo.objects.get(user=self.user).last_name}'

class Transactions(models.Model):
    date = models.DateField(default=timezone.now) 
    amount = models.FloatField()
    user = models.ForeignKey(User , related_name='transaction' , on_delete=models.CASCADE)
    currency = models.ForeignKey(Currencies , related_name='transaction' , on_delete=models.CASCADE)
    act = models.IntegerField()
    def get_user(self):
        return self.user.username
    class meta:
        verbose_name = ' تراکنش  '
        verbose_name_plural = 'تراکنش ها '

class Settings(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    tel = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    telegram = models.CharField(max_length = 300)
    whatsapp = models.CharField(max_length = 300)
    instagram = models.CharField(max_length = 300)
    facebook = models.CharField(max_length = 300)
    logo = models.ImageField(upload_to='settings' , null=True)
    class meta:
        verbose_name = 'تنظیمات'


class Subjects(models.Model):
    date = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User , related_name='Subject' , on_delete=models.CASCADE)
    act = models.IntegerField(null=True , default = 0)
    read = models.BooleanField(default = True)
    title = models.CharField(max_length = 100)
    aread = models.BooleanField(default = False)
    class meta:
        verbose_name = 'سر تیتر تیکت'
        verbose_name_plural = ' سرتیتر های تیکت '
    def get_lastticket(self):
        return self.ticket.all().order_by('-date').first().text

    def get_user(self):
        return self.user.username

    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes
    
class Tickets(models.Model):
    user = models.ForeignKey(User ,related_name='harchi', on_delete=models.CASCADE , null=True)
    date = models.DateTimeField(default=timezone.now)
    subid = models.ForeignKey(Subjects , related_name='ticket' , on_delete=models.CASCADE)
    text = models.CharField(max_length = 1000)
    pic = models.ImageField(upload_to='ticket' , null = True)
    class meta:
        verbose_name = ' تیکت '
        verbose_name_plural = 'تیکت ها'

    def get_pic(self):
        return f'{ROOT}/media/{self.pic}/'

    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_title(self):
        return self.subid.title
    def get_user(self):
        return self.user.username

class ProfitList(models.Model):
    user = models.ForeignKey(User ,related_name='profit', on_delete=models.CASCADE , null=True)
    date = models.DateTimeField(default=timezone.now)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    operation = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.user.username}   ,   amount: {self.amount } {self.currency}   ,   operation:   {self.operation}'

    def get_user(self):
        return self.user.username

    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now()- self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

class Pages(models.Model):
    name = models.CharField(max_length=100, null=True)
    pic = models.ImageField(upload_to='pages' , null = True)
    title = models.CharField(max_length = 100)
    text = models.CharField(max_length = 1000000)
    minitext = models.CharField(max_length = 1000, default='', null=True)
    position = models.CharField(max_length=100 , null=True)
    
    def get_pic(self):
        return f'{ROOT}/media/{self.pic}'

    class meta:
        verbose_name = ' صفحه '
        verbose_name_plural = 'صفحات '

class Forgetrequest(models.Model):
    email = models.CharField(max_length=200,null=True)
    key = models.UUIDField(max_length=100, primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(default=django.utils.timezone.now)

class Price(models.Model):
    rial = models.FloatField(default=1)
    btc = models.FloatField(default=0)
    eth = models.FloatField(default=0)
    trx = models.FloatField(default=0)
    usdt = models.FloatField(default=0)
    doge = models.FloatField(default=0)
    usd = models.FloatField(default=0)

class Leverage(models.Model):
    symbol = models.CharField(max_length=100)
    leverage = models.IntegerField(default=0)
    buymin = models.FloatField(null=True)
    buymax = models.FloatField(null=True)
    sellmin = models.FloatField(null=True)
    sellmax = models.FloatField(null=True)
    def __str__(self):
        return self.symbol


class PriceHistory(models.Model):
    rial = models.FloatField(default=1)
    btc = models.FloatField(default=0)
    eth = models.FloatField(default=0)
    trx = models.FloatField(default=0)
    usdt = models.FloatField(default=0)
    doge = models.FloatField(default=0)
    usd = models.FloatField(default=0)


class Notification(models.Model):
    user = models.ForeignKey(User , related_name='notifications' , on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=300)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

class MainTrades(models.Model):
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    scurrency = models.ForeignKey(Currencies , related_name='sellcurrency', on_delete=models.CASCADE , null=True)
    bcurrency = models.ForeignKey(Currencies , related_name='buycurrency' , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{ROOT}/trades/{self.name}/'
    
    def get_bname(self):
        return self.bcurrency.name
    def get_sname(self):
        return self.scurrency.name


class ProTrades(models.Model):
    name = models.CharField(max_length=100 ,verbose_name=" نام ارز")
    brand = models.CharField(max_length=100 ,null=True,verbose_name=" نماد ارز")
    scurrency = models.ForeignKey(Currencies , related_name='prosellcurrency', on_delete=models.CASCADE , null=True)
    bcurrency = models.ForeignKey(Currencies , related_name='probuycurrency' , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'{ROOT}/trades/{self.name}/'

class MainTradesBuyOrder(models.Model):
    trade = models.ForeignKey(MainTrades, related_name='buyorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='maintradebuyorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 



    def get_brand(self):
        return self.trade.bcurrency.brand

class MainTradesSellOrder(models.Model):
    trade = models.ForeignKey(MainTrades, related_name='sellorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='maintradesellorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 


    def get_brand(self):
        return self.trade.bcurrency.brand
class ProTradesBuyOrder(models.Model):
    trade = models.ForeignKey(ProTrades, related_name='buyorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='protradebuyorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_brand(self):
        return self.trade.bcurrency.brand
class ProTradesSellOrder(models.Model):
    trade = models.ForeignKey(ProTrades, related_name='sellorders' , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='protradesellorders' , on_delete=models.CASCADE)
    amount = models.FloatField()
    price = models.FloatField()
    start = models.FloatField(null=True)
    date = models.DateTimeField(default=timezone.now)
    def get_age(self):
        days=0
        hours=0
        minutes=0
        dif = (timezone.now() - self.date).total_seconds()
        while (dif > 86400):
            dif = dif - 86400
            days = days + 1
        while (dif > 3600):
            dif = dif - 3600
            hours = hours + 1
        while (dif > 60):
            dif = dif - 60
            minutes = minutes + 1


        if hours > 0:
            hours = f' {hours}  ساعت  و'
        else:
            hours = ''


        if minutes > 0:
            minutes = f' {minutes} دقیقه  '
        else:
            minutes = ''



        if days > 0:
            days = f'{days}  روز و '
        else:
            days = ''


        return  days + hours + minutes 

    def get_brand(self):
        return self.trade.bcurrency.brand

class TopSticker(models.Model):
    title = models.ImageField(upload_to='docs' , null = True)
    text = models.CharField(max_length=16 , null=True)
    img = models.BooleanField(default = False)

    def get_image(self):
        return f'{ROOT}/media/{self.img}'


class BottomSticker(models.Model):
    title = models.ImageField(upload_to='docs' , null = True)
    text = models.CharField(max_length=16 , null=True)
    img = models.BooleanField(default = False)

    def get_image(self):
        return f'{ROOT}/media/{self.img}'

class Posts(models.Model):
    title = models.ImageField(upload_to='docs' , null = True)
    text = models.CharField(max_length=16 , null=True)
    img = models.BooleanField(default = False)

    def get_image(self):
        return f'{ROOT}/media/{self.img}'


class News(models.Model):
    title = models.ImageField(upload_to='docs' , null = True)
    text = models.CharField(max_length=16 , null=True)
    img = models.BooleanField(default = False)

    def get_image(self):
        return f'{ROOT}/media/{self.img}'


# Sticking


class Plans(models.Model):
    title = models.CharField(max_length=100)
    currency = models.ForeignKey(Cp_Currencies, related_name='plans', on_delete=models.CASCADE)
    des = models.TextField(max_length=10000)
    percent = models.FloatField(null=True)
    mini = models.FloatField(null=True)
    maxi = models.FloatField(null=True)
    period = models.CharField(null=True , max_length=100)
    
    def __str__(self):
        return f"{self.title} ({self.id})"
        
    class Meta:
        verbose_name = 'پلن ها'
        verbose_name_plural = 'پلن ها'


class UserPlans(models.Model):
    user = models.ForeignKey(User , related_name='userplanssss' , on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans , related_name='plan' , on_delete=models.CASCADE)
    deposit = models.FloatField() 
    option = models.CharField(max_length=100, null=True)
    date_field = models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.userid}   ,   {self.planid}   ,   {self.deposit}   ,   {self.date_field}"

class PlanProfitList(models.Model):
    user = models.ForeignKey(User , related_name='userplans' , on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now) 
    currency = models.ForeignKey(Cp_Currencies, related_name='userplanss', on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans , related_name='userplansss' , on_delete=models.CASCADE)
    amount = models.FloatField()
    def __str__(self):
        return f"{self.userid}{self.invid}"
    