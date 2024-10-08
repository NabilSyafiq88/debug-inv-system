# inventory/urls.py
from django.urls import path
from inventoryapp import views

urlpatterns = [
    path("dash/", views.index, name="dash"),
    path("products/", views.products, name="CellInfo"),
    path("orders/", views.orders, name="GetDebugData"),
    path("users/", views.users, name="users"),
    path("user/", views.user, name="user"),
    path("register/", views.register, name="register"),
]
