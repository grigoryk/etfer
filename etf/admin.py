from django.contrib import admin

from .models import Asset, AssetInvestment, Etf, Portfolio

class AssetInvestmentInline(admin.TabularInline):
    model = AssetInvestment
    extra = 2

@admin.register(Etf)
class EtfAdmin(admin.ModelAdmin):
    list_display = ('short_title', 'title', 'expense_ratio', 'holdings')
    inlines = [AssetInvestmentInline]

admin.site.register(Asset)

admin.site.register(Portfolio)
