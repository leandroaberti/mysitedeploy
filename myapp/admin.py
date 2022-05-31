from django.contrib import admin
from .models import OrderDetail, Product

# Modiify Admin Page
admin.site.site_header = "Buy & Sell Website"
admin.site.site_title = "Admin Buy & Sell"
admin.site.index_title = "Managing Buy & Sell"


#override the Product class
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    search_fields = ('name',)
    list_editable = ('price','description',)
    
    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)   
    actions = ('set_price_to_zero',)

    
# Register your models here.
#admin.site.register(Product)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderDetail)

