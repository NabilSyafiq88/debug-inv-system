from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd

from .forms import SkuForm, FailureForm, FailureData
from .models import CustomUser, Admin, engTech, Operator, cells_Name, Sku_Info, Failure_Mode, Failure_Data, station_Name, model_Name, Failure_Info, Search_PCA
from collections import OrderedDict
from django.db.models import Count

def admin_home(request):
  
  all_cells_count = cells_Name.objects.all().count()
  all_sku_count = Sku_Info.objects.all().count()
  all_failure_mode = Failure_Mode.objects.all().count()
  all_failed_data = Failure_Info.objects.all().count()
  all_station_name = station_Name.objects.all().count()
  model_name = model_Name.objects.all().count()
  
  new_failure = Failure_Info.objects.filter(failure_status = "NEW").count()
  open_item = Failure_Info.objects.filter(failure_status = "OPEN").count()
  close_item= Failure_Info.objects.filter(failure_status = "CLOSED").count()
  
  try:
    complete_percentage = round((close_item/all_failed_data)*100,2)
  except ZeroDivisionError:
    complete_percentage = 0
  
  if new_failure == 0:
    open_percentage = 0
  else:
    open_percentage = round(100 - complete_percentage,2)
  
  #print(complete_percentage)
  #print(open_percentage)
  
  #total failure in each cells
  failure_all = Failure_Info.objects.all()
  #failure_mode_all = Failure_Mode.objects.all()
 
  cells_name_list =[]
  failure_count_list = []
  failure_mode_list = []
  failuremode_count_list = []
  
  for failure in failure_all:
    failures = Failure_Info.objects.filter(test_Cells = failure.test_Cells).count()
    cells_name_list.append(failure.test_Cells)
    failure_count_list.append(failures)

  res = dict(map(lambda i,j : (i,j) , cells_name_list,failure_count_list))

  cells_list = []
  count_list = []
  items = res.items()
  for item in items:
        cells_list.append(item[0]), count_list.append(item[1])
  
  #print (cells_name_list)
  #print (failure_count_list)  
  #print (cells_list)
  #print (count_list)
  
  for failuremode in failure_all:
    failure_Mode = Failure_Info.objects.filter(failure_mode = failuremode.failure_mode).count()
    failure_mode_list.append(failuremode.failure_mode)
    failuremode_count_list.append(failure_Mode)
  
  print(failure_mode_list)
  print(failuremode_count_list)

  
  context={
    "all_cells_count": all_cells_count,
    "all_sku_count": all_sku_count,
    "all_failure_mode":all_failure_mode,
    "all_failed_data":all_failed_data,
    "new_failure":new_failure,
    "open_item":open_item,
    "close_item":close_item,
    #"failures":failures,
    "cells_list":cells_list,
    "count_list":count_list,
    "complete_percentage":complete_percentage,
    "open_percentage":open_percentage,
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

            messages.success(request, "Cells Updated Successfully.")
            return redirect('/edit_cells/'+cells_id)

        except:
            messages.error(request, "Failed to Update Cells.")
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


#SKU portion #############################################################################
def manage_sku(request):
    sku_info = Sku_Info.objects.all()
    context = {
        "sku_info": sku_info
    }
    return render(request, "admin_template/manage_sku_template.html", context) 
  
def add_sku(request):
    cells_name = cells_Name.objects.all()
    model_name = model_Name.objects.all()
    context ={
      "cells_name": cells_name,
      "model_name": model_name
    }
  
    return render(request, "admin_template/add_sku_template.html", context)
  
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
        test_cells = request.POST.get('cells')
        product_family = request.POST.get('model')
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
            sku = Sku_Info(test_Cells=test_cells,
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

def edit_sku(request, sku_id):
    sku = Sku_Info.objects.get(id=sku_id)

    context = {
        "id": sku_id,
        "sku": sku
    }
    print (sku_id)
    #print (cells)
    return render(request, 'admin_template/edit_sku_template.html', context)
  
def edit_sku_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        sku_id = request.POST.get('sku_id')
        sku_name = request.POST.get('sku_cells')
        sku_model = request.POST.get('sku_model')
        sku_FGpartno = request.POST.get('sku_FGpartno')
        sku_FGmodel = request.POST.get('sku_FGmodel')
        sku_PCApartno = request.POST.get('sku_PCApartno')
        sku_status = request.POST.get('sku_status')
        
        print(sku_id)
        print(sku_name)
        print(sku_model)
        print(sku_FGpartno)
        print(sku_FGmodel)
        print(sku_PCApartno)
        print(sku_status)
        
        try:
            sku = Sku_Info.objects.get(id=sku_id)
            sku.FG_PartNo = sku_FGpartno
            sku.FG_Model = sku_FGmodel
            sku.PCA_SN_Number = sku_PCApartno
            sku.product_Status = sku_status
            sku.save()
          

            messages.success(request, "Sku Updated Successfully.")
            return redirect('/edit_sku/'+sku_id)

        except:
            messages.error(request, "Failed to Update Sku.")
            return redirect('/edit_sku/'+sku_id)
          
def delete_sku(request, sku_id):
    sku = Sku_Info.objects.get(id=sku_id)
    try:
        sku.delete()
        messages.success(request, "Sku Deleted Successfully.")
        return redirect('manage_sku')
    except:
        messages.error(request, "Failed to Delete sku.")
        return redirect('manage_sku')    


#Failure mode #################################################################

def manage_failuremode(request):
    failure_mode = Failure_Mode.objects.all()
  
    context = {
        "failure_mode": failure_mode
    }
    return render(request, "admin_template/manage_failuremode_template.html", context)  

def add_failuremode(request):
  
    cells_name = cells_Name.objects.all()
    test_station = station_Name.objects.all()
    print(test_station)
    context ={
      "cells_name": cells_name,
      "station_name":test_station
    }
  
    return render(request, "admin_template/add_failuremode_template.html",context)
  
def add_failuremode_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_failuremode')
    else:
        cells_name = request.POST.get('cells')
        test_station = request.POST.get('test_station')
        failure_mode = request.POST.get('failure_mode')
        
        print (cells_name)
        print(test_station)
        try:
            failure_mode = Failure_Mode(test_Cells=cells_name,test_Station=test_station,failure_Mode=failure_mode)
            failure_mode.save()
            messages.success(request, "Failure Mode Added Successfully!")
            return redirect('add_failuremode')
        except:
            messages.error(request, "Failed to Add Failure Mode!")
            return redirect('add_failuremode')
                                  
def edit_failuremode(request, failuremode_id):
    failure_mode = Failure_Mode.objects.get(id=failuremode_id)
    failuremode_cells = Failure_Mode.objects.get(id=failuremode_id)
    failuremode_station = Failure_Mode.objects.get(id=failuremode_id)
    context = {
        "failuremode_id": failuremode_id,
        "failuremode_cells": failuremode_cells,
        "failuremode_station": failuremode_station,
        "failure_mode": failure_mode
    }
    #print (failure_mode)
    #print (cells)
    return render(request, 'admin_template/edit_failuremode_template.html', context)
  
def edit_failuremode_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        failuremode_id = request.POST.get('failuremode_id')
        failuremode_name = request.POST.get('failure_mode')
        
        print(failuremode_id)
        print(failuremode_name)

        try:
            failuremode = Failure_Mode.objects.get(id=failuremode_id)
            failuremode.failure_Mode = failuremode_name
            failuremode.save()

            messages.success(request, "Failure Mode Updated Successfully.")
            return redirect('/edit_failuremode/'+failuremode_id)

        except:
            messages.error(request, "Failed to Update Failure Mode.")
            return redirect('/edit_failuremode/'+failuremode_id)
          
def delete_failuremode(request, failuremode_id):
    failure_mode = Failure_Mode.objects.get(id=failuremode_id)
    try:
        failure_mode.delete()
        messages.success(request, "Failure Mode Deleted Successfully.")
        return redirect('manage_failuremode')
    except:
        messages.error(request, "Failed to Delete Failure Mode.")
        return redirect('manage_failuremode')    
  
#Failure Data ###################################################################
  
def manage_failuredata(request):
    failure_data = Failure_Data.objects.all()
    context = {
        "failure_data": failure_data
    }
    return render(request, "admin_template/manage_failuredata_template.html", context) 

def add_failuredata(request):
    return render(request, "admin_template/add_failuredata_template.html")
  
#stations portion ##############################################################
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

            messages.success(request, "Station Name Updated Successfully.")
            return redirect('/edit_station/'+station_id)

        except:
            messages.error(request, "Failed to Update Station Name.")
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

#model portion ##############################################################
def manage_model(request):
    model_name = model_Name.objects.all()
    context = {
        "model_name": model_name
    }
    return render(request, "admin_template/manage_model_template.html", context) 
 
def add_model(request):
    return render(request, "admin_template/add_model_template.html")
  
def add_model_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_model')
    else:
        model = request.POST.get('model_name')
        try:
            model_model = model_Name(model_Name=model)
            model_model.save()
            messages.success(request, "Family Model Added Successfully!")
            return redirect('add_model')
        except:
            messages.error(request, "Failed to Add Family Model!")
            return redirect('add_model')
                                  
def edit_model(request, model_id):
    model = model_Name.objects.get(id=model_id)

    context = {
        "id": model_id,
        "model": model
    }
    print (model_id)
    #print (cells)
    return render(request, 'admin_template/edit_model_template.html', context)
  
def edit_model_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        model_id = request.POST.get('model_id')
        model_name = request.POST.get('model_name')
        
        print(model_id)
        print(model_name)

        try:
            model = model_Name.objects.get(id=model_id)
            model.model_Name = model_name
            model.save()

            messages.success(request, "Product Model Updated Successfully.")
            return redirect('/edit_model/'+model_id)

        except:
            messages.error(request, "Failed to Update Product Model.")
            return redirect('/edit_model/'+model_id)
          
def delete_model(request, model_id):
    model = model_Name.objects.get(id=model_id)
    try:
        model.delete()
        messages.success(request, "Product Model Deleted Successfully.")
        return redirect('manage_model')
    except:
        messages.error(request, "Failed to Delete Product Model.")
        return redirect('manage_model')   
      
      
#Failure portion #############################################################################
def manage_failure(request):
    failure_info = Failure_Info.objects.all()
    
    context = {
        "failure_info":failure_info
    }
    return render(request, "admin_template/manage_failure_template.html", context) 
  
  
def add_failure(request):
    cells_name = cells_Name.objects.all()
    test_station = station_Name.objects.all()
    failure_mode = Failure_Mode.objects.all()
    model_name = model_Name.objects.all()
    product_model = Sku_Info.objects.values_list('product_Model',flat=True)
    PCA_no = Sku_Info.objects.values_list('PCA_SN_Number',flat=True)
    #test = sku_info.values()
    #sku_list = []
    #[sku_list.append(x) for x in sku_info if x not in sku_list]
    #sku_list = set(sku_info)
    
    productmodel_list = list(set(product_model))
    productmodel_list.sort()
    
    PCAnumber_list = list(set(PCA_no))
    #PCAnumber_list.sort()
    
    #print(sku_info)
    #print(sort_list)
    #print(model_name)
  
    context ={
      "cells_name": cells_name,
      "station_name":test_station,
      "failure_mode":failure_mode,
      "productmodel_list":productmodel_list,
      "PCAnumber_list":PCAnumber_list,
    }
  
    return render(request, "admin_template/add_failure_template.html", context)
  
def edit_failure(request, sku_id):
    sku = cells_Name.objects.get(id=sku_id)

    context = {
        "id": sku_id,
        "sku": sku
    }
    print (sku_id)
    #print (cells)
    return render(request, 'admin_template/edit_failure_template.html', context)
  
def add_failure_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_failure')
    else:
        product_family = request.POST.get('model')
        test_cells = request.POST.get('cells')
        PCA_Partno = request.POST.get('PCA_PN')
        test_station = request.POST.get('station')
        reject_Bin = request.POST.get('reject_bin')
        failure_Mode = request.POST.get('failure_mode') 
        PCA_Serial = request.POST.get('PCA_Serial')
        
        print(test_cells)
        print(product_family)
        print(reject_Bin)
        print(PCA_Serial)
        print(PCA_Partno)
     
        
        try:
            sku = Failure_Info(test_Cells=test_cells,
                            product_Model=product_family,
                            reject_bin=reject_Bin,
                            PCA_serial=PCA_Serial,
                            PCA_SN_Number=PCA_Partno,
                            test_Station=test_station,
                            failure_mode=failure_Mode,
                            failure_status="OPEN"
                            )
            sku.save()
        
            messages.success(request, "Failure Info Added Successfully!")
            return redirect('add_failure')
        except:
            messages.error(request, "Failed to Add Failure Info!")
            return redirect('add_failure')

def edit_failure(request, failure_id):
    failure = Failure_Info.objects.get(id=failure_id)

    context = {
        "id": failure_id,
        "failure": failure
    }
    print (failure_id)
    #print (cells)
    return render(request, 'admin_template/edit_failure_template.html', context)
  
def edit_failure_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        failure_id = request.POST.get('failure_id')
        failure_cells = request.POST.get('failure_cells')
        failure_model = request.POST.get('failure_model')
        failure_PCApartno = request.POST.get('failure_PCApartno')
        failure_station = request.POST.get('station')
        failure_PCASN = request.POST.get('failure_SN')
        failure_mode = request.POST.get('failure_mode')
        failure_rootcause = request.POST.get('failure_rootcause')
        failure_findings = request.POST.get('failure_findings')
        failure_action = request.POST.get('failure_action')
        failure_status = request.POST.get('status')
        
        print(failure_id)
        print(failure_cells)
        print(failure_model)
        print(failure_PCApartno)
        print(failure_station)
        print(failure_PCASN)
        print(failure_mode)
        print(failure_findings)
        print(failure_findings)
        print(failure_action)
        print(failure_status)
        
        try:
            failure = Failure_Info.objects.get(id=failure_id)
            failure.PCA_serial = failure_PCASN
            failure.root_cause = failure_rootcause
            failure.Findings = failure_findings
            failure.failure_action = failure_action
            
            if failure_action == "Need help":
              failure.failure_status = "OPEN"
            else:
              failure.failure_status = "CLOSED"
            
            failure.save()
          

            messages.success(request, "Reject Info Updated Successfully.")
            return redirect('/edit_failure/'+failure_id)

        except:
            messages.error(request, "Failed to Update Reject Info.")
            return redirect('/edit_failure/'+failure_id)
          
def delete_failure(request, failure_id):
    sku = Failure_Info.objects.get(id=failure_id)
    try:
        sku.delete()
        messages.success(request, "Failure Info Deleted Successfully.")
        return redirect('manage_failure')
    except:
        messages.error(request, "Failed to Delete Failure Info.")
        return redirect('manage_failure')    

#search PCA
def search_PCA(request):
  
  cells_name = cells_Name.objects.all()
  test_station = station_Name.objects.all()
  failure_mode = Failure_Mode.objects.all()
  product_model = Sku_Info.objects.values_list('product_Model',flat=True)
  PCA_no = Sku_Info.objects.values_list('PCA_SN_Number',flat=True)
  
  productmodel_list = list(set(product_model))
  productmodel_list.sort()
    
  PCAnumber_list = list(set(PCA_no))
  
  if 'query' in request.GET:
    query = request.GET['query']
    PCA_SN = Sku_Info.objects.filter(product_Model__iexact=query)

  else:
      PCA_SN = Sku_Info.objects.none()
      
  return render (request, 'admin_template/add_failure_template.html',{'PCA_SN': PCA_SN,'cells_name': cells_name,'station_name':test_station,"failure_mode":failure_mode,'productmodel_list':productmodel_list,'PCAnumber_list':PCAnumber_list})
