from django.contrib import admin
from.models import*

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("id","email", "mobile_number", "is_customer", "is_staff", "is_active")
    search_fields = ("email", "mobile_number")
    list_filter = ("is_customer", "is_staff", "is_active")
    readonly_fields = ("cdate", "mdate")

admin.site.register(CustomUser, CustomUserAdmin)      

class StoreAdmin(admin.ModelAdmin):
    list_display = ("id","name", "owner", "contact_email", "contact_phone")
    search_fields = ("name", "owner__email")
    readonly_fields = ("cdate", "mdate")

admin.site.register(Store, StoreAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name", "slug", "store")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("cdate", "mdate")

admin.site.register(Category, CategoryAdmin)


class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name", "category", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("cdate", "mdate")

admin.site.register(Subcategory, SubcategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ("image", "alt_text", "order")
    readonly_fields = ("cdate", "mdate")


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "store", "price", "inventory_count")
    search_fields = ("name", "sku")
    list_filter = ("store", "category", "subcategory")
    readonly_fields = ("cdate", "mdate")
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)


class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "order")
    search_fields = ("product__name",)
    readonly_fields = ("cdate", "mdate")


admin.site.register(ProductImage, ProductImageAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","id", "user", "store", "total_amount", "status")
    list_filter = ("status", "store")
    search_fields = ("id", "user__email")
    readonly_fields = ("cdate", "mdate")


admin.site.register(Order, OrderAdmin)

class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ("id","order", "product", "sku", "quantity", "unit_price")
    readonly_fields = ("cdate", "mdate")

admin.site.register(OrderDetail, OrderDetailAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id","invoice_number", "order", "amount", "issued_at")
    search_fields = ("invoice_number",)
    list_filter = ("issued_at",)
    readonly_fields = ("cdate", "mdate")


admin.site.register(Invoice, InvoiceAdmin)



