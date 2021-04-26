from django.contrib import admin

from .models import Asset, AssetInEtf, Etf, Portfolio, EtfProvider, RawData, EtfInPortfolio

class AssetInvestmentInline(admin.TabularInline):
    model = AssetInEtf
    extra = 2

@admin.register(Etf)
class EtfAdmin(admin.ModelAdmin):
    list_display = (
        'provider', 'name', 'holdings_last_updated', 'inception_date',
        'shares_outstanding', 'expense_ratio', 'holdings'
    )
    inlines = [AssetInvestmentInline]

class AssetAdmin(admin.ModelAdmin):
    list_display = (
        'ticker', 'name', 'location', 'sector', 'asset_class', 'exchange', 'currency', 'fx_rate', 'market_currency'
    )
    list_filter = (
        'location', 'sector', 'asset_class', 'exchange', 'currency', 'market_currency'
    )
    search_fields = ['name', 'ticker']
admin.site.register(Asset, AssetAdmin)

class EtfInPortfolioInline(admin.TabularInline):
    model = EtfInPortfolio
    extra = 2

class PortfolioAdmin(admin.ModelAdmin):
    inlines = [EtfInPortfolioInline]

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(EtfProvider)

class RawDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'provider')
admin.site.register(RawData, RawDataAdmin)
