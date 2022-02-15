from django.contrib import admin
from .models import Regions, PricingRules


@admin.register(Regions)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name',)


@admin.register(PricingRules)
class PricingRulesAdmin(admin.ModelAdmin):
    list_display = ('min_price', 'max_price', 'procent', 'is_active')

