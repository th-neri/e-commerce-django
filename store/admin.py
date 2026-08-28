from django.contrib import admin, messages
from django.db.models import Count, QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

#to add filter to products with low, ok, and high inventory
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('low', 'Low'),
            ('ok', 'Ok'),
            ('high', 'High')
        ]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == 'low':
            return queryset.filter(inventory__lte=10)

        if self.value() == 'ok':
            return queryset.filter(inventory__gt=10, inventory__lte=20)

        if self.value() == 'high':
            return queryset.filter(inventory__gt=20)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product_count']
    ordering = ['title']
    search_fields = ['title']

    #to count the quantity of products of every collection and provide the link to the product page
    #where you can see every product of a specific collection
    @admin.display(ordering='product_count') 
    def product_count(self, collection):
        url = (reverse('admin:store_product_changelist')
                + '?'
                + urlencode({
                    'collection_id': str(collection.id)
                }))
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields= {
        'slug': ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    ordering = ['title']
    list_per_page = 15

    def collection_title(self, product):
        return product.collection.title

    def inventory_status(self, product):
        if product.inventory <= 10:
            return 'Low'
        elif product.inventory <=20:
            return 'Ok'
        else:
            return 'High'

    #a customized action to update(clear) the inventory of products
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{update_count} product(s) were successfully updated!',
            messages.ERROR
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'total_orders']
    list_editable = ['membership']
    ordering = ['first_name']
    list_per_page = 15
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    #to count the quantity of orders of every customer and provide the link to the customer page
    #where you can see every order of a specific customer
    @admin.display(ordering='total_orders')
    def total_orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer_id': str(customer.id)
               }))
        return format_html('<a href="{}">{}</a>', url, customer.total_orders)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            total_orders=Count('order')
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['placed_at', 'payment_status', 'customer']
    list_editable = ['payment_status']
    ordering = ['placed_at']
    list_per_page = 15


