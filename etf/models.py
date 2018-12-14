from django.db import models
from django.conf import settings

class Asset(models.Model):
    title = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    finclass = models.CharField(max_length=100, blank=True, null=True)
    sector = models.CharField(max_length=100, blank=True, null=True)

class Etf(models.Model):
    title = models.CharField(max_length=500)
    short_title = models.CharField(max_length=20)
    expense_ratio = models.DecimalField(max_digits=4, decimal_places=3)
    assets = models.ManyToManyField(Asset, through="AssetInvestment")

    def holdings(self):
        return self.assets.count()

class AssetInvestment(models.Model):
    etf = models.ForeignKey(Etf, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    etfs = models.ManyToManyField(Etf, through='EtfInvestment')

class EtfInvestment(models.Model):
    investment = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    etf = models.ForeignKey(Etf, on_delete=models.CASCADE)
    percentage = models.DecimalField(max_digits=4, decimal_places=2)
