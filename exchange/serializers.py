from chat.models import ChatSession
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import  BottomSticker, Cp_Currencies, Cp_Wallet, Cp_Withdraw, CpDepositRequest, General, LevelFee, Leverage, MainTradesBuyOrder, MainTradesSellOrder, News, PerpetualRequest, Posts, ProTradesBuyOrder, ProTradesSellOrder , ProTrades , MainTrades, Notification, ProfitList, TopSticker, VerifyAcceptRequest , VerifyMelliRequest , BankAccounts , VerifyBankAccountsRequest , Price , Currencies, Forgetrequest, UserInfo, Wallet, Verify, BankCards, Transactions, Settings , Subjects , Tickets, Pages, VerifyBankRequest, Staff, WithdrawRequest, buyoutrequest, buyrequest, exchangerequest, selloutrequest, sellrequest

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = (
            "id",
            "first_name",
            "last_name",
            "mobile",
            "smsverify",
            "googleverify",
            "phone",
            "email",
            "level",
            "address",
            "is_active",
            "is_admin",
            "is_staff",
            "get_melli",
            "get_mellip",
            "get_otp",
            "referalid",
            "get_referal"
        )

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "rial",
            "btc",
            "eth",
            "trx",
            "usdt",
            "doge",
            "usd",
        )
class BuySerializer(serializers.ModelSerializer):
    class Meta:
        model = buyrequest
        fields = (
            "id",
            "get_user",
            "get_age",
            "user",
            "currency",
            "ramount",
            "rramount",
            "camount",
            "date",
            "act"
        )
class BuyoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = buyoutrequest
        fields = (
            "id",
            "get_user",
            "get_age",
            "user",
            "address",
            "currency",
            "ramount",
            "rramount",
            "camount",
            "date",
            "act"
        )
class selloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = selloutrequest
        fields = (
            "id",
            "get_user",
            "get_age",
            "user",
            "hash",
            "currency",
            "ramount",
            "rramount",
            "camount",
            "date",
            "act"
        )
class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = sellrequest
        fields = (
            "id",
            "get_user",
            "get_age",
            "user",
            "currency",
            "ramount",
            "camount",
            "date",
            "act"
        )

class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = exchangerequest
        fields = (
            "id",
            "get_user",
            "get_age",
            "user",
            "currency",
            "currency2",
            "camount",
            "camount2",
            "date",
            "act"
        )

class LeverageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leverage
        fields = (
            "symbol",
            "leverage",
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )

class CpWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cp_Wallet
        fields = (
            "id",
            "currency",
            "address",
        )

class CpDepositRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CpDepositRequest
        fields = (
            "id",
            "user",
            "get_user",
            "hash",
            "currency",
            "get_age",
            "amount",
            "act",
        )
        
class CpCurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cp_Currencies
        fields = (
            "id",
            "name",
            "brand",
            "chain",
            "can_deposit",
            "can_withdraw",
            "deposit_least_amount",
            "withdraw_least_amount",
            "withdraw_tx_fee",
        )
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = (
            "id",
            "currency",
            "amount",
            "address",
            "get_currency"
        )
class CurrenciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = (
            "id",
            "name",
            "brand",
            "get_image"
        )
class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Verify
        fields = (
            "mobilev",
            "emailv",
            "melliv",
            "idv",
            "acceptv",
            "bankv",
            "accountv",
            "rulev",
            "coinv",
            "isphone",
            "get_acceptphoto",
            "get_melliphoto"
        )
class LevelFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LevelFee
        fields = (
            "id",
            "buy",
            "sell",
            "perpetual",
            "margin",
            "exchange",
        )

class VerifyMelliRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyMelliRequest
        fields = (
            "id",
            "user",
            "melliimg",
            "mellic",
            "action",
            "get_image",
            "get_user",
            "get_user_id"
        )

class VerifyAcceptRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyAcceptRequest
        fields = (
            "id",
            "user",
            "acceptimg",
            "get_image",
            "action",
            "get_user",
            "get_user_id"
        )

class BankCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankCards
        fields = (
            "user",
            "number",
            "status"
        )

class BankAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = (
            "id",
            "user",
            "number",
            "shebac",
            "status"
        )

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = (
            "user",
            "level",
        )

class VerifyBankRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyBankRequest
        fields = (
            "id",
            "user",
            "bankc",
            "get_user",
            "action",
            "get_first",
            "get_last"
        )

class VerifyBankAccountsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyBankAccountsRequest
        fields = (
            "id",
            "user",
            "bankc",
            "shebac",
            "get_user",
            "action",
            "get_first",
            "get_last"
        )

class TransactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = (
            "date",
            "amount",
            "user",
            "currency",
            "act",
            "get_user"
        )


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = (
            "id",
            "name",
            "address",
            "tel",
            "email",
            "telegram",
            "whatsapp",
            "instagram",
            "facebook",
            "logo"
        )

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = (
            "id",
            "date",
            "user",
            "act",
            "read",
            "title",
            "aread",
            "get_age",
            "get_user",
            "get_lastticket"
        )
class TicketsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tickets
        fields = (
            "date",
            "pic",
            "user",
            "get_pic",
            "subid",
            "text",
            "get_age",
            "get_title",
            "get_user"
        )


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = (
            "id",
            "title",
            "text",
            "minitext",
            "pic",
            "position",
            "get_pic"
        )
class ForgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forgetrequest
        fields = (
            "email",
        )

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            "title",
            "text",
            "seen",
            "get_age",
        )

class MainTradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTrades
        fields = (
            "id",
            "name",
            "brand",
            "get_bname",
            "get_sname"
        )

class ProTradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTrades
        fields = (
            "id",
            "name",
            "brand",
        )

class ProTradesSellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTradesSellOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class ProTradesBuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProTradesBuyOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class MainTradesSellOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTradesSellOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class MainTradesBuyOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainTradesBuyOrder
        fields = (
            "trade",
            "amount",
            "price",
            "start",
            "date",
            "get_age",
            "get_brand"
        )

class Cp_WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cp_Withdraw
        fields = (
            "id",
            "date",
            "user",
            "currency",
            "chain",
            "amount",
            "address",
            "get_currency",
            "get_age",
            "get_user"
        )

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = WithdrawRequest
        fields = (
            "id",
            "date",
            "user",
            "amount",
            "bankaccount",
            "get_age",
            "get_user",
            "get_sheba",
            "get_number"
        )

class GeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = General
        fields = (
            "name",
            "email",
            "mobile",
            "whatsapp",
            "telegram",
            "instagram",
            "telephone",
            "rule",
            "logo",
        )
class PerpetualRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerpetualRequest
        fields = (
            "id",
            "user",
            "get_age",
            "get_user",
        )

class ProfitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitList
        fields = (
            "id",
            "user",
            "amount",
            "currency",
            "operation",
            "get_age",
            "get_user",
        )

class AdminChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatSession
        fields = (
            "id",
            "owner",
            "uri",
            "email",
            "get_user",
            "get_seen"
        )

class TopStickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopSticker
        fields = (
            "id",
            "title",
            "text",
            "get_image"
        )

class BottomStickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BottomSticker
        fields = (
            "id",
            "title",
            "text",
            "get_image"
        )

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = (
            "id",
            "title",
            "text",
            "get_image"
        )

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = (
            "id",
            "title",
            "text",
            "get_image"
        )