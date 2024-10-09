# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventoryapp.forms import UserRegistry, SkuForm, FailureForm
from inventoryapp.models import Sku_Info, Failure_Mode


#@login_required
#def index(request):
    #orders_user = Failure_Mode.objects.all()
    #users = User.objects.all()[:2]
    #orders_adm = Failure_Mode.objects.all()[:2]
    #products = Sku_Info.objects.all()[:2]
    #reg_users = len(User.objects.all())
    #all_prods = len(Sku_Info.objects.all())
    #all_orders = len(Failure_Mode.objects.all())
    #context = {
        #"title": "Home",
        #"orders": orders_user,
        #"orders_adm": orders_adm,
        #"users": users,
        #"products": products,
        #"count_users": reg_users,
        #"count_products": all_prods,
        #"count_orders": all_orders,
    #}
    #return render(request, "inventory/index.html", context)


#@login_required
#def products(request):
    #products = Sku_Info.objects.all()
    #if request.method == "POST":
        #form = SkuForm(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect("products")
    #else:
        #form = SkuForm()
    #context = {"title": "Products", "products": products, "form": form}
    #return render(request, "inventory/products.html", context)


#@login_required
#def orders(request):
    #orders = Failure_Mode.objects.all()
    #print([i for i in request])
    #if request.method == "POST":
        #form = FailureForm(request.POST)
        #if form.is_valid():
            #instance = form.save(commit=False)
            #instance.created_by = request.user
            #instance.save()
            #return redirect("orders")
    #else:
        #form = FailureForm()
    #context = {"title": "Orders", "orders": orders, "form": form}
    #return render(request, "inventory/orders.html", context)


#@login_required
#def users(request):
    #users = User.objects.all()
    #context = {"title": "Users", "users": users}
    #return render(request, "inventory/users.html", context)


#@login_required
#def user(request):
    #context = {"profile": "User Profile"}
    #return render(request, "inventory/user.html", context)


#def register(request):
    #if request.method == "POST":
        #form = UserRegistry(request.POST)
        #if form.is_valid():
            #form.save()
            #return redirect("login")
    #else:
        #form = UserRegistry()
    #context = {"register": "Register", "form": form}
    #return render(request, "inventory/register.html", context)
  
  
def search_PCA_SN (request):
  if 'query' in request.GET:
      query = request.GET['query']
      PCA_SN = Sku_Info.objects.filter(PCA_SN_Number__iexact=query)
  else:
      PCA_SN = Sku_Info.objects.none()
  return render (request, 'index.html',{'PCA_SN': PCA_SN})
