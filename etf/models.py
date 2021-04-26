from django.db import models
from django.conf import settings

from abc import ABC

class WithName(models.Model):
    name = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class EtfProvider(WithName):
    pass

class Country(WithName):
    pass

class Sector(WithName):
    pass

class AssetClass(WithName):
    pass

class Exchange(WithName):
    pass

class Currency(WithName):
    pass

class RawData(models.Model):
    data = models.TextField()
    provider = models.ForeignKey(EtfProvider, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    overrides = models.TextField(blank=True, null=True, default="""{
    "asset":{},
    "etf": {}
}""")

    def __str__(self):
        return "Raw data from %s" % self.provider

class Asset(models.Model):
    ticker = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=500, blank=True, null=True)

    cusip = models.CharField(max_length=100, blank=True, null=True)
    isin = models.CharField(max_length=100, blank=True, null=True)
    sedol = models.CharField(max_length=100, blank=True, null=True)

    location = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, blank=True, null=True)
    asset_class = models.ForeignKey(AssetClass, on_delete=models.CASCADE, blank=True, null=True)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey(Currency, related_name="currency", on_delete=models.CASCADE, blank=True, null=True)
    fx_rate = models.FloatField(blank=True, null=True)
    market_currency = models.ForeignKey(Currency, related_name="market_currency", on_delete=models.CASCADE, blank=True, null=True)

class Etf(WithName):
    provider = models.ForeignKey(EtfProvider, on_delete=models.CASCADE)

    holdings_last_updated = models.DateField(blank=True, null=True)
    inception_date = models.DateField(blank=True, null=True)

    shares_outstanding = models.PositiveIntegerField(blank=True, null=True)
    expense_ratio = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)

    assets = models.ManyToManyField(Asset, through="AssetInEtf")

    class Meta:
        unique_together = [['provider', 'name']]

    def holdings(self):
        return self.assets.count()

class AssetInEtf(models.Model):
    etf = models.ForeignKey(Etf, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    market_value = models.DecimalField(max_digits=100, decimal_places=3, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    notional_value = models.DecimalField(max_digits=100, decimal_places=3, blank=True, null=True)
    shares = models.DecimalField(max_digits=100, decimal_places=3, blank=True, null=True)

    def price(self):
        return self.market_value / self.shares

class Portfolio(WithName):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    etfs = models.ManyToManyField(Etf, through='EtfInPortfolio')
    value = models.DecimalField(max_digits=100, decimal_places=3, blank=True, null=True)

class EtfInPortfolio(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    etf = models.ForeignKey(Etf, on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=3)
