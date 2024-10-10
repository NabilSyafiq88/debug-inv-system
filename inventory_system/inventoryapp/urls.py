# inventory/urls.py
from django.contrib import admin
from django.urls import path
from inventoryapp import views

urlpatterns = [
    #path("dash/", views.index, name="dash"),
    #path("products/", views.products, name="Sku_Info"),
    #path("orders/", views.orders, name="Failure_Mode"),
    #path("users/", views.users, name="users"),
    #path("user/", views.user, name="user"),
    #path("register/", views.register, name="register"),
    
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('contact', views.contact, name="contact"),
    path('login', views.loginUser, name="login"),
    #path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path("find/", views.search_PCA_SN, name="find"),
]
