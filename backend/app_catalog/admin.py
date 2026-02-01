from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'work_schedule')
    list_filter = ('city',)
    search_fields = ('city', 'address')
    ordering = ('city', 'address')
