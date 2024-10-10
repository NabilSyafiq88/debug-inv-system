# inventory/views.py
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventoryapp.forms import UserRegistry, SkuForm, FailureForm
from inventoryapp.models import Sku_Info, Failure_Mode, CustomUser, engTech, Operator, Admin
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
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
 
def home(request):
    return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

def loginUser(request):
    return render(request, 'login_page.html')
  
def doLogin(request):
    
    print("here")
    user_name = request.GET.get('username')
    password = request.GET.get('password')
    # user_type = request.GET.get('user_type')
    print(user_name)
    print(password)
    print(request.user)
    if not (user_name and password):
        messages.error(request, "Please provide all the details!!")
        return render(request, 'login_page.html')
    
    user = CustomUser.objects.filter(username=user_name, password=password).last()
    if not user:
        messages.error(request, 'Invalid Login Credentials!!')
        return render(request, 'login_page.html')

    login(request, user)
    print(request.user)
    
    if user.user_type == CustomUser.OPERATOR:
        return redirect('operator_home/')
    elif user.user_type == CustomUser.ENGTECH:
        return redirect('engtech_home/')
    elif user.user_type == CustomUser.ADMIN:
        return redirect('admin_home/')

    return render(request, 'home.html')

def registration(request):
    return render(request, 'registration.html')

def doRegistration(request):
    user_name = request.GET.get('username')
    #last_name = request.GET.get('last_name')
    #email_id = request.GET.get('email')
    password = request.GET.get('password')
    confirm_password = request.GET.get('confirmPassword')

    print(user_name)
    print(password)
    print(confirm_password)
    #print(first_name)
    #print(last_name)
    if not (user_name and password and confirm_password):
        messages.error(request, 'Please provide all the details!!')
        return render(request, 'registration.html')
      
    is_user_exists = CustomUser.objects.filter(username=user_name).exists()

    if is_user_exists:
        messages.error(request, 'User with this username already exists. Please proceed to login!!')
        return render(request, 'registration.html')

    user_type = get_user_type_from_username(user_name)
    
    if user_type is None:
        messages.error(request, "Please use valid format for the username: '<username>.<engtech|operator>'")
        return render(request, 'registration.html')

    #username = user_name.split('.')[0]

    #if CustomUser.objects.filter(username=user_name).exists():
        #messages.error(request, 'User with this username already exists. Please use different username')
        #return render(request, 'registration.html')

    user = CustomUser()
    user.username = user_name
    #user.email = email_id
    user.password = password
    user.user_type = user_type
    #user.first_name = first_name
    #user.last_name = last_name
    user.save()
    
    if user_type == CustomUser.ENGTECH:
        engTech.objects.create(admin=user)
    elif user_type == CustomUser.OPERATOR:
        Operator.objects.create(admin=user)
    elif user_type == CustomUser.ADMIN:
        Admin.objects.create(admin=user)
    return render(request, 'login_page.html')
  
def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')
  
 
def search_PCA_SN (request):
  if 'query' in request.GET:
      query = request.GET['query']
      PCA_SN = Sku_Info.objects.filter(PCA_SN_Number__iexact=query)
  else:
      PCA_SN = Sku_Info.objects.none()
  return render (request, 'index.html',{'PCA_SN': PCA_SN})

def get_user_type_from_username(user_name):

    try:
        #email_id = email_id.split('@')[0]
        username_user_type = user_name.split('.')[1]
        return CustomUser.EMAIL_TO_USER_TYPE_MAP[username_user_type]
    except:
        return None