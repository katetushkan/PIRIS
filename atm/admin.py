from django.contrib import admin

# Register your models here.
from atm.models import CreditCard


class CardAdmin(admin.ModelAdmin):
    exclude = ()


admin.site.register(CreditCard, CardAdmin)