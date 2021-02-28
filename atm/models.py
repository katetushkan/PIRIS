import os

from binascii import hexlify

from django.db import models

from piris.models import CreditAccount


def _createHash():
    """This function generate 10 character long hash"""
    return hexlify(os.urandom(5))


class CreditCard(models.Model):
    card_number = models.CharField(max_length=16)
    account_id = models.ForeignKey(CreditAccount, on_delete=models.CASCADE, related_name='credit_card')
    pin = models.CharField(max_length=10, default=_createHash, unique=True)
