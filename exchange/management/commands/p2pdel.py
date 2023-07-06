from exchange.models import P2pRequest
from django.core.management.base import BaseCommand, CommandError
import requests
from .lib import CoinexPerpetualApi
import time
from .lib.coinex import CoinEx

class Command(BaseCommand):
    def handle(self, *args, **options):
        for item in P2pRequest.objects.all():
            item.delete()