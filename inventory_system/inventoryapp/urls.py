# inventory/urls.py
from django.urls import path
from inventoryapp import views

urlpatterns = [
    #path("dash/", views.index, name="dash"),
    #path("products/", views.products, name="Sku_Info"),
    #path("orders/", views.orders, name="Failure_Mode"),
    #path("users/", views.users, name="users"),
    #path("user/", views.user, name="user"),
    #path("register/", views.register, name="register"),
    path("find/", views.search_PCA_SN, name="find"),
]
