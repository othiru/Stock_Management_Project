from django.contrib import admin
from .models import *
from .forms import *



class StockCreateAdmin(admin.ModelAdmin):
   list_display = ["category", "item_name", "quantity"]
   form = StockCreateForm
#    list_filter = ["category"]
#    search_fields = ["category", "item_name"]

class CategoryCreateAdmin(admin.ModelAdmin):
   list_display = ["name"]
   # form = CategoryCreateForm
#    list_filter = ["name"]
#    search_fields = ["name"]

# Register your models here.
admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category, CategoryCreateAdmin)
