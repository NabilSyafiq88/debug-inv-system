from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import SkuForm, FailureForm, FailureData
from .models import CustomUser, Admin, engTech, Operator, cells_Name, Sku_Info, Failure_Mode, Failure_Data, station_Name

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
  
#cells portion
def manage_cells(request):
    cells_name = cells_Name.objects.all()
    context = {
        "cells_name": cells_name
    }
    return render(request, "admin_template/manage_cells_template.html", context) 
 
def add_cells(request):
    return render(request, "admin_template/add_cells_template.html")
  
def add_cells_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_cells')
    else:
        cells = request.POST.get('cells_name')
        print (cells)
        try:
            cells_model = cells_Name(cell_Name=cells)
            cells_model.save()
            messages.success(request, "Cells Added Successfully!")
            return redirect('add_cells')
        except:
            messages.error(request, "Failed to Add Cells!")
            return redirect('add_cells')
          
def edit_cells(request, cells_id):
    cells = cells_Name.objects.get(id=cells_id)

    context = {
        "id": cells_id,
        "cells": cells
    }
    print (cells_id)
    #print (cells)
    return render(request, 'admin_template/edit_cells_template.html', context)
  
def edit_cells_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        cells_id = request.POST.get('cells_id')
        cells_name = request.POST.get('cells_name')
        
        print(cells_id)
        print(cells_name)
  

        try:
            cells = cells_Name.objects.get(id=cells_id)
            cells.cell_Name = cells_name
            cells.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_cells/'+cells_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_cells/'+cells_id)
          
def delete_cells(request, cells_id):
    cells = cells_Name.objects.get(id=cells_id)
    try:
        cells.delete()
        messages.success(request, "Cells Deleted Successfully.")
        return redirect('manage_cells')
    except:
        messages.error(request, "Failed to Delete Cells.")
        return redirect('manage_cells')    


#SKU portion
def manage_sku(request):
    sku_info = Sku_Info.objects.all()
    context = {
        "sku_info": sku_info
    }
    return render(request, "admin_template/manage_sku_template.html", context) 
  
def add_sku(request):
    return render(request, "admin_template/add_sku_template.html")
  
def edit_sku(request, sku_id):
    sku = cells_Name.objects.get(id=sku_id)

    context = {
        "id": sku_id,
        "sku": sku
    }
    print (sku_id)
    #print (cells)
    return render(request, 'admin_template/edit_sku_template.html', context)
  
def add_sku_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_sku')
    else:
        product_status = request.POST.get('product_status')
        test_cells = request.POST.get('test_cells')
        product_family = request.POST.get('product_family')
        FG_partno = request.POST.get('FGpartno')
        FG_model = request.POST.get('FGmodel')
        PCA_Partno = request.POST.get('PCA_PN')
        
        print(product_status)
        print(test_cells)
        print(product_family)
        print(FG_partno)
        print(FG_model)
        print(PCA_Partno)
        try:
            sku = Sku_Info(test_Cells_id=test_cells,
                            product_Model=product_family,
                            FG_PartNo=FG_partno,
                            FG_Model=FG_model,
                            PCA_SN_Number=PCA_Partno,
                            product_Status =product_status)
            sku.save()
        
            messages.success(request, "SKU Added Successfully!")
            return redirect('add_sku')
        except:
            messages.error(request, "Failed to Add SKU!")
            return redirect('add_sku')

#for Failure mode

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

    


  
def add_failuremode(request):
    return render(request, "admin_template/add_failuremode_template.html")
  
def add_failuredata(request):
    return render(request, "admin_template/add_failuredata_template.html")
  
#for stations portion
def manage_station(request):
    station_name = station_Name.objects.all()
    context = {
        "station_name": station_name
    }
    return render(request, "admin_template/manage_station_template.html", context) 
 
def add_station(request):
    return render(request, "admin_template/add_station_template.html")
  
def add_station_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_station')
    else:
        station = request.POST.get('station_name')
        try:
            station_model = station_Name(station_Name=station)
            station_model.save()
            messages.success(request, "Station Added Successfully!")
            return redirect('add_station')
        except:
            messages.error(request, "Failed to Add Station!")
            return redirect('add_station')
                         
          
def edit_station(request, station_id):
    station = station_Name.objects.get(id=station_id)

    context = {
        "id": station_id,
        "station": station
    }
    print (station_id)
    #print (cells)
    return render(request, 'admin_template/edit_station_template.html', context)
  
def edit_station_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        station_id = request.POST.get('station_id')
        station_name = request.POST.get('station_name')
        
        print(station_id)
        print(station_name)
  

        try:
            station = station_Name.objects.get(id=station_id)
            station.station_Name = station_name
            station.save()

            messages.success(request, "Course Updated Successfully.")
            return redirect('/edit_station/'+station_id)

        except:
            messages.error(request, "Failed to Update Course.")
            return redirect('/edit_station/'+station_id)
          
def delete_station(request, station_id):
    station = station_Name.objects.get(id=station_id)
    try:
        station.delete()
        messages.success(request, "Station Deleted Successfully.")
        return redirect('manage_station')
    except:
        messages.error(request, "Failed to Delete Station.")
        return redirect('manage_station')    
