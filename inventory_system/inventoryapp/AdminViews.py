from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
import pandas as pd
from django.template import loader

from .forms import SkuForm, FailureForm, FailureData
from .models import CustomUser, Admin, Operator, root_Cause, action_Taken, cells_Name, Sku_Info, Failure_Mode, Failure_Data, station_Name, model_Name, Failure_Info, Search_PCA
from collections import OrderedDict
from django.db.models import Count, Q

from django.utils import timezone
import pytz

timezone.activate(pytz.timezone("Asia/Singapore"))

def admin_home(request):
  
  print("Admin Home")
  print(request.user.username)
  
  all_cells_count = cells_Name.objects.all().count()
  all_sku_count = Sku_Info.objects.all().count()
  all_failure_mode = Failure_Mode.objects.all().count()
  all_failed_data = Failure_Info.objects.all().count()
  all_station_name = station_Name.objects.all().count()
  model_name = model_Name.objects.all().count()
  
  new_failure = Failure_Info.objects.filter(failure_status = "NEW").count()
  open_item = Failure_Info.objects.filter(failure_status = "OPEN").count()
  close_item= Failure_Info.objects.filter(failure_status = "CLOSED").count()
  escalation_item = Failure_Info.objects.filter(failure_Category = "Escalation").count()
  reject_item = all_failed_data - escalation_item
  
  
  try:
    complete_percentage = round((close_item/all_failed_data)*100,2)
  except ZeroDivisionError:
    complete_percentage = 0
  
  if open_item == 0:
    open_percentage = 0
  else:
    open_percentage = round(100 - complete_percentage,2)
  
  #print(complete_percentage)
  #print(open_percentage)
  
  #total failure in each cells
  failure_all = Failure_Info.objects.all()
  all_action_count = Failure_Info.objects.all()
  #failure_mode_all = Failure_Mode.objects.all()
 
  #cells_name_list =[]
  #failure_count_list = []
  failure_mode_list = []
  failuremode_count_list = []
  
  #for failure in failure_all:
    #failures = Failure_Info.objects.filter(test_Cells = failure.test_Cells).count()
    #cells_name_list.append(failure.test_Cells)
    #failure_count_list.append(failures)

  #res = dict(map(lambda i,j : (i,j) , cells_name_list,failure_count_list))
  Escalation_open = Failure_Info.objects.filter(failure_status = "OPEN",failure_Category = "Escalation").count()
  Escalation_close = escalation_item - Escalation_open
  
  Reject_open = Failure_Info.objects.filter(failure_status = "OPEN",failure_Category__isnull = True).count()
  Reject_close = reject_item - Reject_open
  #cells_name_list.append(failure.test_Cells)
  #failure_count_list.append(failures)

  #cells_list = []
  #count_list = []
  #items = res.items()
  #for item in items:
        #cells_list.append(item[0]), count_list.append(item[1])
  
  #print (cells_name_list)
  #print (failure_count_list)  
  #print (cells_list)
  print (Escalation_open)
  print (Escalation_close)
  print (Reject_open)
  print (Reject_close)
  
  #for failuremode in failure_all:
    #failure_Mode = Failure_Info.objects.filter(failure_mode = failuremode.failure_mode).count()
    #failure_mode_list.append(failuremode.failure_mode)
    #failuremode_count_list.append(failure_Mode)
  
  #print(failure_mode_list)
  #print(failuremode_count_list)

  
  context={
    "all_cells_count": all_cells_count,
    "all_sku_count": all_sku_count,
    "all_failure_mode":all_failure_mode,
    "all_failed_data":all_failed_data,
    "new_failure":new_failure,
    "open_item":open_item,
    "close_item":close_item,
    "escalation_item":escalation_item,
    "reject_item":reject_item,
    "Escalation_open":Escalation_open,
    "Escalation_close":Escalation_close,
    "Reject_open":Reject_open,
    "Reject_close":Reject_close,
    #"failures":failures,
    #"cells_list":cells_list,
    #"count_list":count_list,
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
        return redirect('manage_cells')
    else:
        cells = request.POST.get('cells_name')
        print (cells)
        try:
            cells_model = cells_Name(cell_Name=cells)
            cells_model.save()
            messages.success(request, "Cells Added Successfully!")
            return redirect('manage_cells')
        except:
            messages.error(request, "Failed to Add Cells!")
            return redirect('manage_cells')
          
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
            return redirect('manage_cells')

        except:
            messages.error(request, "Failed to Update Cells.")
            #return redirect('/edit_cells/'+cells_id)
            return redirect('manage_cells')
          
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
        return redirect('manage_sku')
    else:
        product_status = request.POST.get('product_status')
        test_cells = request.POST.get('cells')
        product_family = request.POST.get('model')
        PCA_Price = request.POST.get('PCAprice')
        FG_model = request.POST.get('FGmodel')
        PCA_Partno = request.POST.get('PCA_PN')
        
        print(product_status)
        print(test_cells)
        print(product_family)
        print(PCA_Price)
        print(FG_model)
        print(PCA_Partno)
        try:
            sku = Sku_Info(test_Cells=test_cells,
                            product_Model=product_family,
                            PCA_Price_USD=PCA_Price,
                            FG_Model=FG_model,
                            PCA_SN_Number=PCA_Partno,
                            product_Status =product_status)
            sku.save()
        
            messages.success(request, "SKU Added Successfully!")
            return redirect('manage_sku')
        except:
            messages.error(request, "Failed to Add SKU!")
            return redirect('manage_sku')

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
        sku_PCAprice = request.POST.get('sku_PCAprice')
        sku_FGmodel = request.POST.get('sku_FGmodel')
        sku_PCApartno = request.POST.get('sku_PCApartno')
        sku_status = request.POST.get('sku_status')
        
        print(sku_id)
        print(sku_name)
        print(sku_model)
        print(sku_PCAprice)
        print(sku_FGmodel)
        print(sku_PCApartno)
        print(sku_status)
        
        try:
            sku = Sku_Info.objects.get(id=sku_id)
            sku.PCA_Price_USD = sku_PCAprice
            sku.FG_Model = sku_FGmodel
            sku.PCA_SN_Number = sku_PCApartno
            sku.product_Status = sku_status
            sku.save()
          

            messages.success(request, "Sku Updated Successfully.")
            return redirect('manage_sku')

        except:
            messages.error(request, "Failed to Update Sku.")
            return redirect('manage_sku')
          
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
        return redirect('manage_failuremode')
    else:
        cells_name = request.POST.get('cells')
        test_station = request.POST.get('test_station')
        Failure_mode = request.POST.get('failure_mode')
        
        try:
            failure_mode = Failure_Mode(test_Cells=cells_name,test_Station=test_station,failure_Mode = Failure_mode)
            failure_mode.save()
            messages.success(request, "Failure Mode Added Successfully!")
            return redirect('manage_failuremode')
        except:
            messages.error(request, "Failed to Add Failure Mode!")
            return redirect('manage_failuremode')
                                  
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
            return redirect('manage_failuremode')

        except:
            messages.error(request, "Failed to Update Failure Mode.")
            return redirect('manage_failuremode')
          
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
        return redirect('manage_station')
    else:
        station = request.POST.get('station_name')
        try:
            station_model = station_Name(station_Name=station)
            station_model.save()
            messages.success(request, "Station Added Successfully!")
            return redirect('add_station')
        except:
            messages.error(request, "Failed to Add Station!")
            return redirect('manage_station')
                                  
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
            return redirect('manage_station')

        except:
            messages.error(request, "Failed to Update Station Name.")
            return redirect('manage_station')
          
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
        return redirect('manage_model')
    else:
        model = request.POST.get('model_name')
        try:
            model_model = model_Name(model_Name=model)
            model_model.save()
            messages.success(request, "Family Model Added Successfully!")
            return redirect('manage_model')
        except:
            messages.error(request, "Failed to Add Family Model!")
            return redirect('manage_model')
                                  
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
            return redirect('manage_model')

        except:
            messages.error(request, "Failed to Update Product Model.")
            return redirect('manage_model')
          
def delete_model(request, model_id):
    model = model_Name.objects.get(id=model_id)
    try:
        model.delete()
        messages.success(request, "Product Model Deleted Successfully.")
        return redirect('manage_model')
    except:
        messages.error(request, "Failed to Delete Product Model.")
        return redirect('manage_model')   
      
#Escalate portion #############################################################################
def manage_escalate(request):
    failure_info = Failure_Info.objects.all()
    
    context = {
        "failure_info":failure_info
    }
    return render(request, "admin_template/manage_escalate_template.html", context) 
  
#edit_escalation
def edit_escalate(request, failure_id):
    failure = Failure_Info.objects.get(id=failure_id)
    action_taken = action_Taken.objects.all()
    root_cause = root_Cause.objects.all()

    context = {
        "id": failure_id,
        "failure": failure,
        "action_taken":action_taken,
        "root_cause":root_cause
    }
    print (failure_id)
    #print (action_taken)
    return render(request, 'admin_template/edit_escalate_template.html', context)
  
  #delete_escalation
def delete_escalate(request, failure_id):
    sku = Failure_Info.objects.get(id=failure_id)
    try:
        sku.delete()
        messages.success(request, "Escalation Info Deleted Successfully.")
        return redirect('manage_escalate')
    except:
        messages.error(request, "Failed to Delete Escalation Info.")
        return redirect('manage_escalate')  
      
  #edit_escalation_save
  
def edit_escalate_save(request):
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
        
        #print(failure_id)
        #print(failure_cells)
        #print(failure_model)
        #print(failure_PCApartno)
        #print(failure_station)
        #print(failure_PCASN)
        #print(failure_mode)
        print(failure_findings)
        print(failure_action)
        print(failure_status)
        
        try:
            failure = Failure_Info.objects.get(id=failure_id)
            failure.PCA_serial = failure_PCASN
            failure.root_cause = failure_rootcause
            failure.Findings = failure_findings
            failure.failure_action = failure_action
            
            if failure_action == "Escalate" or failure_action == "None":
              failure.failure_status = "OPEN"
            else:
              failure.failure_status = "CLOSED"
            
            failure.save()
          

            messages.success(request, "Escalation Info Updated Successfully.")
            return redirect('manage_escalate')

        except:
            messages.error(request, "Failed to Update Escalation Info.")
            return redirect('manage_escalate')
  
      
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
    FG_model = Sku_Info.objects.values_list('FG_Model',flat=True)
    PCA_no = Sku_Info.objects.values_list('PCA_SN_Number',flat=True)
    #F_mode = Failure_Mode.objects.filter(test_Cells = "LEPTON").values()
    #test = sku_info.values()
    #sku_list = []
    #[sku_list.append(x) for x in sku_info if x not in sku_list]
    #sku_list = set(sku_info)
    
    FGmodel_list = list(set(FG_model))
    FGmodel_list.sort()
    
    PCAnumber_list = list(set(PCA_no))
    #PCAnumber_list.sort()
    
    #print(sku_info)
    #print(sort_list)
    #print(model_name)
  
    context ={
      "cells_name": cells_name,
      "station_name":test_station,
      "failure_mode":failure_mode,
      "productmodel_list":FGmodel_list,
      "PCAnumber_list":PCAnumber_list,
    }
  
    return render(request, "admin_template/add_failure_template.html", context)
   
def add_failure_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_failure')
    else:
        product_family = request.POST.get('FG_model')
        test_cells = request.POST.get('cells')
        PCA_Partno = request.POST.get('PCA_PN')
        test_station = request.POST.get('station')
        PCA_Price = request.POST.get('PCA_price')
        test_station = request.POST.get('Test_Station') 
        failure_Mode = request.POST.get('failure_mode') 
        PCA_Serial = request.POST.get('PCA_Serial')
        
        print(test_cells)
        print(product_family)
        print(PCA_Price)
        print(PCA_Serial)
        print(PCA_Partno)
        print(test_station)
        print(failure_Mode)
        
        #x = failure_Mode.split(" | ")
        #print (x)
        #print (x[0])
        #print (x[1])
        #print (x[2])

        #test_station = x[0]
        #failure_Mode = x[1]
     
        
        try:
            sku = Failure_Info(test_Cells=test_cells,
                            product_Model=product_family,
                            PCA_Price_USD=PCA_Price,
                            PCA_serial=PCA_Serial,
                            PCA_SN_Number=PCA_Partno,
                            test_Station=test_station,
                            failure_mode=failure_Mode,
                            failure_status="OPEN"
                            )
            sku.save()
        
            messages.success(request, "Reject Info Added Successfully!")
            return redirect('manage_failure')
        except:
            messages.error(request, "Failed to Add Reject Info!")
            return redirect('manage_failure')

def edit_failure(request, failure_id):
    failure = Failure_Info.objects.get(id=failure_id)
    action_taken = action_Taken.objects.all()
    root_cause = root_Cause.objects.all()

    context = {
        "id": failure_id,
        "failure": failure,
        "action_taken":action_taken,
        "root_cause":root_cause
    }
    print (failure_id)
    #print (action_taken)
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
        failure_PCA_price = request.POST.get('failure_PCA_Price')
        
        
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
        print(failure_PCA_price)
        
        try:
            failure = Failure_Info.objects.get(id=failure_id)
            failure.PCA_serial = failure_PCASN
            failure.root_cause = failure_rootcause
            failure.Findings = failure_findings
            failure.failure_action = failure_action
            failure.PCA_Price_USD = failure_PCA_price
            
            if failure_action == "None":
              failure.failure_status = "OPEN"
            elif failure_action == "Escalate":
              failure.failure_status = "OPEN"
              failure.failure_Category = "Escalation"
              failure.escalation_Date = timezone.localtime(timezone.now())
            else:
              failure.failure_status = "CLOSED"
            
            failure.save()
          

            messages.success(request, "Reject Info Updated Successfully.")
            return redirect('manage_failure')

        except:
            messages.error(request, "Failed to Update Reject Info.")
            return redirect('manage_failure')
          
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
  FG_model = Sku_Info.objects.values_list('FG_Model',flat=True)
  PCA_no = Sku_Info.objects.values_list('PCA_SN_Number',flat=True)
  F_Station = ""
  
  FGmodel_list = list(set(FG_model))
  FGmodel_list.sort()
    
  PCAnumber_list = list(set(PCA_no))
  
  if 'query' in request.GET:
    query = request.GET['query']
    print(query)
    F_Station = request.GET['F_Station']
    print(F_Station)
    
    PCA_SN = Sku_Info.objects.filter(FG_Model__iexact=query)
    F_cells = PCA_SN.values_list('test_Cells',flat=True)
    F_cells = ''.join(F_cells)
    F_mode = Failure_Mode.objects.filter(test_Cells = F_cells,test_Station = F_Station).values()
  else:
      PCA_SN = Sku_Info.objects.none()
      F_mode = Failure_Mode.objects.none()
       
  return render (request, 'admin_template/add_failure_template.html',{'PCA_SN': PCA_SN,'cells_name': cells_name,'station_name':test_station,"failure_mode":failure_mode,'FGmodel_list':FGmodel_list,'PCAnumber_list':PCAnumber_list,'F_mode':F_mode,'F_Station':F_Station})

#Actions portion ##############################################################
def manage_action(request):
    action_taken = action_Taken.objects.all()
    context = {
        "action_taken": action_taken
    }
    return render(request, "admin_template/manage_action_template.html", context) 
 
def add_action(request):
    return render(request, "admin_template/add_action_template.html")
  
def add_action_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_action')
    else:
        action = request.POST.get('action_taken')
        try:
            action_taken = action_Taken(action_Taken=action)
            action_taken.save()
            messages.success(request, "Action Taken Added Successfully!")
            return redirect('manage_action')
        except:
            messages.error(request, "Failed to Add Action Taken!")
            return redirect('manage_action')
                                  
def edit_action(request, action_id):
    action = action_Taken.objects.get(id=action_id)

    context = {
        "action_id": action_id,
        "action": action
    }
    print (action_id)
    #print (cells)
    return render(request, 'admin_template/edit_action_template.html', context)
  
def edit_action_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        action_id = request.POST.get('action_id')
        action_taken = request.POST.get('action_taken')
        
        print(action_id)
        print(action_taken)

        try:
            action = action_Taken.objects.get(id=action_id)
            action.action_Taken = action_taken
            action.save()

            messages.success(request, "Action Taken Updated Successfully.")
            #return redirect('/edit_action/'+action_id)
            return redirect('manage_action')

        except:
            messages.error(request, "Failed to Update Action Taken.")
            #return redirect('/edit_action/'+action_id)
            return redirect('manage_action')
          
def delete_action(request, action_id):
    action = action_Taken.objects.get(id=action_id)
    try:
        action.delete()
        messages.success(request, "Action Taken Deleted Successfully.")
        return redirect('manage_action')
    except:
        messages.error(request, "Failed to Delete Action Taken.")
        return redirect('manage_action')  
      
#Actions portion ##############################################################
def manage_rootcause(request):
    root_cause = root_Cause.objects.all()
    context = {
        "root_cause": root_cause
    }
    return render(request, "admin_template/manage_rootcause_template.html", context) 
 
def add_rootcause(request):
    return render(request, "admin_template/add_rootcause_template.html")
  
def add_rootcause_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_rootcause')
    else:
        rootcause = request.POST.get('root_cause')
        try:
            root_cause = root_Cause(root_Cause=rootcause)
            root_cause.save()
            messages.success(request, "Root Cause Added Successfully!")
            return redirect('manage_rootcause')
        except:
            messages.error(request, "Failed to Add Root Cause!")
            return redirect('manage_rootcause')
                                  
def edit_rootcause(request, rootcause_id):
    rootcause = root_Cause.objects.get(id=rootcause_id)

    context = {
        "rootcause_id": rootcause_id,
        "rootcause": rootcause
    }
    print (rootcause_id)
    #print (cells)
    return render(request, 'admin_template/edit_rootcause_template.html', context)
  
def edit_rootcause_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        rootcause_id = request.POST.get('rootcause_id')
        rootcause = request.POST.get('root_cause')
        
        print(rootcause_id)
        #print(rootcause)

        try:
            root_cause = root_Cause.objects.get(id=rootcause_id)
            root_cause.root_Cause = rootcause
            root_cause.save()

            messages.success(request, "Root Cause Updated Successfully.")
            #return redirect('/edit_action/'+action_id)
            return redirect('manage_rootcause')

        except:
            messages.error(request, "Failed to Update Root Cause.")
            #return redirect('/edit_action/'+action_id)
            return redirect('manage_rootcause')
          
def delete_rootcause(request, rootcause_id):
    root_cause = root_Cause.objects.get(id=rootcause_id)
    try:
        root_cause.delete()
        messages.success(request, "Root Cause Deleted Successfully.")
        return redirect('manage_rootcause')
    except:
        messages.error(request, "Failed to Delete Root Cause.")
        return redirect('manage_rootcause')  