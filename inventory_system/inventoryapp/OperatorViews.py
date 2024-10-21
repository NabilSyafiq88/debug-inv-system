from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
# will store media or photos
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object

from .models import CustomUser, cells_Name, Failure_Info, station_Name, Failure_Mode, model_Name, Sku_Info, Operator


def operator_home(request):
  print("Operator Home")
  print(request.user.id)
  operator_obj = Operator.objects.get(admin=request.user.id)
  print("yiha")
  print(operator_obj)
    
  all_cells_count = cells_Name.objects.all().count()
  all_sku_count = Sku_Info.objects.all().count()
  all_failure_mode = Failure_Mode.objects.all().count()
  all_failed_data = Failure_Info.objects.all().count()
  all_station_name = station_Name.objects.all().count()
  model_name = model_Name.objects.all().count()
  
  new_failure = Failure_Info.objects.filter(failure_status = "NEW").count()
  open_item = Failure_Info.objects.filter(failure_status = "OPEN").count()
  close_item= Failure_Info.objects.filter(failure_status = "CLOSED").count()
  
  complete_percentage = (close_item/all_failed_data)*100
  open_percentage = 100 - complete_percentage
  
#total failure in each cells
  failure_all = Failure_Info.objects.all()
  failure_list = Failure_Info.objects.values_list('test_Cells',flat=True)
  
  failure_cell_list = list(set(failure_list))
  
  #print (failure_all)
   
  cells_name_list =[]
  failure_count_list = []
  
  for failure in failure_all:
    failures = Failure_Info.objects.filter(test_Cells = failure.test_Cells).count()
    cells_name_list.append(failure.test_Cells)
    failure_count_list.append(failures)

  res = dict(map(lambda i,j : (i,j) , cells_name_list,failure_count_list))

  #print (res)
  
  cells_list = []
  count_list = []
  items = res.items()
  for item in items:
        cells_list.append(item[0]), count_list.append(item[1])
  
  print (cells_name_list)
  print (failure_count_list)  
  print (cells_list)
  print (count_list)
  
  sku_info_list = []
  failure_info_list = []
  
  context={
    "all_cells_count": all_cells_count,
    "all_sku_count": all_sku_count,
    "all_failure_mode":all_failure_mode,
    "all_failed_data":all_failed_data,
    "new_failure":new_failure,
    "open_item":open_item,
    "close_item":close_item,
    "failures":failures,
    "cells_list":cells_list,
    "count_list":count_list,
    "complete_percentage":complete_percentage,
    "open_percentage":open_percentage,
  }

  return render(request, "operator_template/operator_home_template.html",context)

#Failure portion #############################################################################
def opt_manage_failure(request):
    failure_info = Failure_Info.objects.all()
    
    context = {
        "failure_info":failure_info
    }
    return render(request, "operator_template/opt_manage_failure_template.html", context) 
  
  
def opt_add_failure(request):
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
  
    return render(request, "operator_template/opt_add_failure_template.html", context)
  
def opt_edit_failure(request, sku_id):
    sku = cells_Name.objects.get(id=sku_id)

    context = {
        "id": sku_id,
        "sku": sku
    }
    print (sku_id)
    #print (cells)
    return render(request, 'operator_template/opt_edit_failure_template.html', context)
  
def opt_add_failure_save(request):
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
            return redirect('opt_add_failure')
        except:
            messages.error(request, "Failed to Add Failure Info!")
            return redirect('opt_add_failure')

def opt_edit_failure(request, failure_id):
    failure = Failure_Info.objects.get(id=failure_id)

    context = {
        "id": failure_id,
        "failure": failure
    }
    print (failure_id)
    #print (cells)
    return render(request, 'operator_template/opt_edit_failure_template.html', context)
  
def opt_edit_failure_save(request):
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
            return redirect('/opt_edit_failure/'+failure_id)

        except:
            messages.error(request, "Failed to Update Reject Info.")
            return redirect('/opt_edit_failure/'+failure_id)
          
def opt_delete_failure(request, failure_id):
    sku = Failure_Info.objects.get(id=failure_id)
    try:
        sku.delete()
        messages.success(request, "Failure Info Deleted Successfully.")
        return redirect('opt_manage_failure')
    except:
        messages.error(request, "Failed to Delete Failure Info.")
        return redirect('opt_manage_failure')    

def opt_search_PCA(request):
  
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
      
  return render (request, 'operator_template/opt_add_failure_template.html',{'PCA_SN': PCA_SN,'cells_name': cells_name,'station_name':test_station,"failure_mode":failure_mode,'productmodel_list':productmodel_list,'PCAnumber_list':PCAnumber_list})





