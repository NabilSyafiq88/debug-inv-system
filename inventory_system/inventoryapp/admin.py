# inventory/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from inventoryapp.models import Sku_Info, Failure_Mode, cells_Name, Failure_Data, CustomUser, Admin, engTech, Operator

admin.site.site_header = "Inventory Management System"


class SkuAdmin(admin.ModelAdmin):
    model = Sku_Info
    list_display = ("test_Cells", "product_Model","FG_PartNo" ,"FG_Model", "PCA_SN_Number","product_Status")
    list_filter = ["product_Model"]
    search_fields = ["PCA_SN_Number"]


class FailureAdmin(admin.ModelAdmin):
    model = Failure_Mode
    list_display = ("test_Cells", "test_Station","failure_Mode")
    list_filter = ["test_Cells"]
    search_fields = ["test_Station"]
    
class CellAdmin(admin.ModelAdmin):
    model = cells_Name
    list_display = ("cell_Name", "date_registered")
    #list_filter = ["date"]
    search_fields = ["cell_Name"]
    
class FailureDataAdmin(admin.ModelAdmin):
    model = Failure_Data
    list_display = ("test_Cells", "test_Station","failure_Mode")
    #list_filter = ["date"]
    search_fields = ["test_Station"]
    
class UserModel(UserAdmin):
    pass

admin.site.register(CustomUser, UserModel)
admin.site.register(Sku_Info, SkuAdmin)
admin.site.register(Failure_Mode, FailureAdmin)
admin.site.register(cells_Name, CellAdmin)
admin.site.register(Failure_Data, FailureDataAdmin)
admin.site.register(Admin)
admin.site.register(engTech)
admin.site.register(Operator)
