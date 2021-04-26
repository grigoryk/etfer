from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RawData, Etf, Asset, AssetInEtf, Country, Sector, AssetClass, Exchange, Currency
from django.db import IntegrityError, transaction

from decimal import Decimal
from io import StringIO
from datetime import datetime
import csv

processors = {
    "iSHARES": {
        "date_format": "%b %d, %Y",
        "fields": 18,
        "first": "Ticker",
        "etf": {
            "name": 0,
            "as_of_date": 1,
            "inception_date": 2,
            "shares_outstanding": 3,
        },
        "asset": {
            "ticker": 0,
            "name": 1,
            "sector": 2,
            "class": 3,
            "market_value": 4,
            "weight": 5,
            "notional_value": 6,
            "shares": 7,
            "cusip": 8,
            "isin": 9,
            "sedol": 10,
            "price": 11,
            "location": 12,
            "exchange": 13,
            "currency": 14,
            "fx_rate": 15,
            "market_currency": 16,
            "accrual_date": 17,
        }
    },
    "BlackRock": {
        "date_format": "%b %d, %Y",
        "fields": 10,
        "first": "Ticker",
        "etf": {
            "name": 0,
            "as_of_date": 1,
            "inception_date": 2,
            "shares_outstanding": 4,
        },
        "asset": {
            "ticker": 0,
            "name": 1,
            "sector": 7,
            "market_value": 5,
            "weight": 2,
            "notional_value": 6,
            "shares": 4,
            "cusip": 8,
            "price": 3,
            "exchange": 9,
        }
    },
    "BlackRock2": {
        "date_format": "%b %d, %Y",
        "fields": 15,
        "first": "Ticker",
        "etf": {
            "name": 0,
            "as_of_date": 1,
            "inception_date": 2,
            "shares_outstanding": 4,
        },
        "asset": {
            "ticker": 0,
            "name": 1,
            "sector": 7,
            # "class": 3,
            "market_value": 5,
            "weight": 2,
            "notional_value": 6,
            "shares": 4,
            "cusip": 9,
            # "isin": 9,
            "sedol": 8,
            "price": 3,
            "location": 11,
            "exchange": 10,
            "currency": 12,
            "fx_rate": 14,
            "market_currency": 13,
            # "accrual_date": 17,
        }
    },
    "SPDR": {
        "date_format": "%d-%b-%Y",
        "fields": 8,
        "first": "Name",
        "etf": {
            "name": 0,
            "as_of_date": 1
        },
        "asset": {
            "ticker": 1,
            "name": 0,
            "sector": 5,
            # "class": 3,
            # "market_value": 4,
            "weight": 4,
            # "notional_value": 6,
            "shares": 6,
            "cusip": 2,
            # "isin": 9,
            "sedol": 3,
            # "price": 11,
            # "location": 12,
            # "exchange": 13,
            # "currency": 14,
            # "fx_rate": 15,
            "market_currency": 7,
            # "accrual_date": 17,
        }
    }
}

@receiver(post_save, sender=RawData, dispatch_uid="process_raw_data_once")
def process_raw_data(sender, instance: RawData, **kwargs):
    f = StringIO(instance.data)
    reader = csv.reader(f)

    if instance.provider.name == "iSHARES":
        process_with_format(instance, reader, processors["iSHARES"])

    elif instance.provider.name == "BlackRock":
        process_with_format(instance, reader, processors["BlackRock"])

    elif instance.provider.name == "BlackRock2":
        process_with_format(instance, reader, processors["BlackRock2"])

    elif instance.provider.name == "SPDR":
        process_with_format(instance, reader, processors["SPDR"])

def process_with_format(instance, reader, fmt):
    reader = list(reader)

    etf_fmt = fmt["etf"]
    name = reader[etf_fmt["name"]][0]
    etf, _ = Etf.objects.get_or_create(name=name, provider=instance.provider)

    holdings_as_of = reader[etf_fmt["as_of_date"]][1]
    etf.holdings_last_updated = datetime.strptime(holdings_as_of, fmt["date_format"])

    if "inception_date" in etf_fmt:
        inception_date = reader[etf_fmt["inception_date"]][1]
        etf.inception_date = datetime.strptime(inception_date, fmt["date_format"])

    if "shares_outstanding" in etf_fmt:
        shares_outstanding = reader[etf_fmt["shares_outstanding"]][1]
        etf.shares_outstanding = int(float(shares_outstanding.replace(',', '')))

    etf.save()

    overrides = eval(instance.overrides)
    asset_overrides = overrides["asset"]
    asset_fmt = fmt["asset"]

    for row in reader:
        if len(row) != fmt["fields"] or row[0] == fmt["first"]:
            continue

        asset, _ = Asset.objects.get_or_create(ticker=row[asset_fmt["ticker"]])

        if not asset.name:
            asset.name = row[asset_fmt["name"]]

        if not asset.cusip and "cusip" in asset_fmt:
            asset.cusip = row[asset_fmt["cusip"]]

        if not asset.isin and "isin" in asset_fmt:
            asset.isin = row[asset_fmt["isin"]]

        if not asset.sedol and "sedol" in asset_fmt:
            asset.sedol = row[asset_fmt["sedol"]]

        if not asset.location and "location" in asset_overrides:
            asset.location = Country.objects.get_or_create(name=asset_overrides["location"])[0]
        elif not asset.location and "location" in asset_fmt:
            asset.location = Country.objects.get_or_create(name=row[asset_fmt["location"]])[0]

        if not asset.exchange and "exchange" in asset_fmt:
            asset.exchange = Exchange.objects.get_or_create(name=row[asset_fmt["exchange"]])[0]

        if not asset.sector and "sector" in asset_fmt:
            asset.sector = Sector.objects.get_or_create(name=row[asset_fmt["sector"]])[0]

        if not asset.asset_class and "class" in asset_fmt:
            asset.asset_class = AssetClass.objects.get_or_create(name=row[asset_fmt["class"]])[0]

        if not asset.currency and "currency" in asset_fmt:
            asset.currency = Currency.objects.get_or_create(name=row[asset_fmt["currency"]])[0]

        if not asset.market_currency and "market_currency" in asset_fmt:
            asset.market_currency = Currency.objects.get_or_create(name=row[asset_fmt["market_currency"]])[0]

        if not asset.fx_rate and "fx_rate" in asset_fmt:
            asset.fx_rate = float(row[asset_fmt["fx_rate"]].replace(',', ''))

        asset.save()

        try:
            with transaction.atomic():
                asset_in_etf, _ = AssetInEtf.objects.get_or_create(
                    asset=asset,
                    etf=etf
                )
                if "weight" in asset_fmt:
                    asset_in_etf.weight = Decimal(row[asset_fmt["weight"]].replace(',', ''))

                if "market_value" in asset_fmt:
                    asset_in_etf.market_value = Decimal(row[asset_fmt["market_value"]].replace(',', ''))

                if "notional_value" in asset_fmt:
                    asset_in_etf.notional_value = Decimal(row[asset_fmt["notional_value"]].replace(',', ''))

                if "shares" in asset_fmt:
                    asset_in_etf.shares = Decimal(row[asset_fmt["shares"]].replace(',', ''))

                asset_in_etf.save()
        except IntegrityError:
            # TODO
            pass

# def process_ishares(instance: RawData):
#     f = StringIO(instance.data)
#     reader = csv.reader(f)

#     date_format = "%b %d, %Y"

#     name = next(reader)[0]
#     holdings_as_of = next(reader)[1]
#     inception_date = next(reader)[1]
#     shares_outstanding = next(reader)[1]

#     etf, _ = Etf.objects.get_or_create(name=name, provider=instance.provider)
#     etf.inception_date = datetime.strptime(inception_date, date_format)
#     etf.holdings_last_updated = datetime.strptime(holdings_as_of, date_format)
#     etf.shares_outstanding = int(float(shares_outstanding.replace(',', '')))
#     etf.save()

#     for row in reader:
#         if len(row) != 18 or row[0] == "Ticker":
#             continue
#         asset, _ = Asset.objects.get_or_create(name=row[1], ticker=row[0])

#         asset.cusip = row[8]
#         asset.isin = row[9]
#         asset.sedol = row[10]

#         asset.location = Country.objects.get_or_create(name=row[12])[0]
#         asset.exchange = Exchange.objects.get_or_create(name=row[13])[0]
#         asset.sector = Sector.objects.get_or_create(name=row[2])[0]
#         asset.asset_class = AssetClass.objects.get_or_create(name=row[3])[0]
#         asset.currency = Currency.objects.get_or_create(name=row[14])[0]
#         asset.market_currency = Currency.objects.get_or_create(name=row[16])[0]
#         asset.fx_rate = float(row[15])
#         asset.save()

#         try:
#             with transaction.atomic():
#                 asset_in_etf, _ = AssetInEtf.objects.get_or_create(
#                     asset=asset,
#                     etf=etf
#                 )
#                 asset_in_etf.weight = Decimal(row[5].replace(',', ''))
#                 asset_in_etf.market_value = Decimal(row[4].replace(',', ''))
#                 asset_in_etf.notional_value = Decimal(row[6].replace(',', ''))
#                 asset_in_etf.shares = Decimal(row[7].replace(',', ''))

#                 asset_in_etf.save()
#         except IntegrityError:
#             # TODO
#             pass
