from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import SkuForm, FailureForm, FailureData
from .models import CustomUser, Admin, engTech, Operator, cells_Name, Sku_Info, Failure_Mode, Failure_Data

def admin_home(request):
  
  all_cells_count = cells_Name.objects.all().count()
  all_sku_count = Sku_Info.objects.all().count()
  all_failure_mode = Failure_Mode.objects.all().count()
  all_failed_data = Failure_Data.objects.all().count()
  cells_name_list =[]
  sku_info_list = []
  failure_info_list = []
  
  context={
    "all_cells_count": all_cells_count,
    "all_sku_count": all_sku_count,
    "all_failure_mode":all_failure_mode,
    "all_failed_data":all_failed_data,
  }
  
  return render(request,"admin_template/home_content.html",context)
  
  
def manage_cells(request):
    cells_name = cells_Name.objects.all()
    context = {
        "cells_name": cells_name
    }
    return render(request, "admin_template/manage_cells_template.html", context) 

def manage_sku(request):
    sku_info = Sku_Info.objects.all()
    context = {
        "sku_info": sku_info
    }
    return render(request, "admin_template/manage_sku_template.html", context)  
  
def manage_failuremode(request):
    failure_mode = Failure_Mode.objects.all()
    context = {
        "failure_mode": failure_mode
    }
    return render(request, "admin_template/manage_failuremode_template.html", context)  
  
def manage_failuredata(request):
    failure_data = Failure_Data.objects.all()
    context = {
        "failure_data": failure_data
    }
    return render(request, "admin_template/manage_failuredata_template.html", context) 