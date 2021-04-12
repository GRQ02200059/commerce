from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.User)
admin.site.register(models.Auction_lists)
admin.site.register(models.Bids)
admin.site.register(models.Comments)
admin.site.register(models.Watchlists)