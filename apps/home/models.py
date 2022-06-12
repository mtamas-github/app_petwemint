# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - PetWeMint
"""
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CryptoAccount(models.Model):

    class Meta:
        db_table = "crypto_accounts"

    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    address = models.CharField(max_length=50)
    mnemonic = models.CharField(max_length=100)
    created = models.DateTimeField()


class NFTPrepared(models.Model):

    class Meta:
        db_table = "nft_prepared"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.CharField(max_length=100)
    data = models.TextField()


class NFTMinted(models.Model):

    class Meta:
        db_table = "nft_final"

    account = models.ForeignKey(CryptoAccount, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    prepared = models.ForeignKey(NFTPrepared, on_delete=models.RESTRICT)
    uuid = models.UUIDField()
    location = models.CharField(maxlength=250)
    url = models.CharField(max_length=150)
