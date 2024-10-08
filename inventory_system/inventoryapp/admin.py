# inventory/admin.py
from django.contrib import admin
from inventoryapp.models import failureInfo, getDebugData, UserProfile

admin.site.site_header = "Inventory Management System"


class ProductAdmin(admin.ModelAdmin):
    model = failureInfo
    list_display = ("test_Cells","model", "failure_Station","failure_Description","failure_date")
    list_filter = ["failure_date"]
    search_fields = ["model"]


class OrderAdmin(admin.ModelAdmin):
    model = getDebugData
    list_display = ("info", "order_quantity", "date")
    list_filter = ["date"]
    search_fields = ["info"]

class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("user", "physical_address", "mobile", "picture")
    list_filter = ["user"]
    search_fields = ["user"]


admin.site.register(failureInfo, ProductAdmin)
admin.site.register(getDebugData, OrderAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
