"""
URL configuration for inventory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# IMS/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import include, path
from inventoryapp.views import search_PCA_SN, home, contact, loginUser, doLogin, registration, doRegistration
from inventoryapp import AdminViews

urlpatterns = [
    path("/", include("inventoryapp.urls")),
    path("admin/", admin.site.urls),
    path('', home, name="home"),
    path('contact', contact, name="contact"),
    path('login', loginUser, name="login"),
    path('doLogin', doLogin, name="doLogin"),
    path('registration', registration, name="registration"),
    path('doRegistration', doRegistration, name="doRegistration"),
    
    #path(
        #"", auth.LoginView.as_view(template_name="inventory/login.html"), name="login"
    #),
    #path(
        #"logout/",
        #auth.LogoutView.as_view(template_name="inventory/logout.html"),
        #name="logout",
    #),
    path('', search_PCA_SN, name='search_PCA_SN'),
    
    #Admin page
    path('admin_home/', AdminViews.admin_home, name="admin_home"),
    

    #failuredata
    path('manage_failuredata/', AdminViews.manage_failuredata, name="manage_failuredata"),
    
    #cells
    path('manage_cells/', AdminViews.manage_cells, name="manage_cells"),
    path('add_cells/', AdminViews.add_cells, name="add_cells"),
    path('add_cells_save/', AdminViews.add_cells_save, name="add_cells_save"),
    path('edit_cells/<cells_id>', AdminViews.edit_cells, name="edit_cells"),
    path('edit_cells_save/', AdminViews.edit_cells_save, name="edit_cells_save"),
    path('delete_cells/<cells_id>/', AdminViews.delete_cells, name="delete_cells"),
    
    #sku
    path('manage_sku/', AdminViews.manage_sku, name="manage_sku"),
    path('add_sku/', AdminViews.add_sku, name="add_sku"),
    path('add_sku_save/', AdminViews.add_sku_save, name="add_sku_save"),
    path('edit_sku/<sku_id>', AdminViews.edit_sku, name="edit_sku"),
    path('edit_sku_save/', AdminViews.edit_sku_save, name="edit_sku_save"),
    path('delete_sku/<sku_id>/', AdminViews.delete_sku, name="delete_sku"),

    
    #station
    path('manage_station/', AdminViews.manage_station, name="manage_station"),
    path('add_station/', AdminViews.add_station, name="add_station"),
    path('add_station_save/', AdminViews.add_station_save, name="add_station_save"),    
    path('edit_station/<station_id>', AdminViews.edit_station, name="edit_station"),
    path('edit_station_save/', AdminViews.edit_station_save, name="edit_station_save"),
    path('delete_station/<station_id>/', AdminViews.delete_station, name="delete_station"),
    
    #failuremode
    path('manage_failuremode/', AdminViews.manage_failuremode, name="manage_failuremode"),   
    path('add_failuremode/', AdminViews.add_failuremode, name="add_failuremode"),
    path('add_failuremode_save/', AdminViews.add_failuremode_save, name="add_failuremode_save"),    
    path('edit_failuremode/<failuremode_id>', AdminViews.edit_failuremode, name="edit_failuremode"),
    path('edit_failuremode_save/', AdminViews.edit_failuremode_save, name="edit_failuremode_save"),
    path('delete_failuremode/<failuremode_id>/', AdminViews.delete_failuremode, name="delete_failuremode"),
    
    #model
    path('manage_model/', AdminViews.manage_model, name="manage_model"),   
    path('add_model/', AdminViews.add_model, name="add_model"),
    path('add_model_save/', AdminViews.add_model_save, name="add_model_save"),    
    path('edit_model/<model_id>', AdminViews.edit_model, name="edit_model"),
    path('edit_model_save/', AdminViews.edit_model_save, name="edit_model_save"),
    path('delete_model/<model_id>/', AdminViews.delete_model, name="delete_model"),

        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
