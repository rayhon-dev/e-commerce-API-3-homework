from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('price',)
    can_delete = True

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'status', 'total', 'items_count')
    list_filter = ('status', 'user')
    search_fields = ('order_number', 'user__phone', 'user__username')
    readonly_fields = ('order_number', 'total', 'items_count')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal')
    search_fields = ('product__title',)
    readonly_fields = ('subtotal',)
