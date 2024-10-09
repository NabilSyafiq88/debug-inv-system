# inventory/models.py
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django import forms

FAILURE_STATION = (
    ("PCA Burn IN", "PCA Burn IN"),
    ("Calibration", "Calibration"),
    ("Final Test", "Final Test"),
    ("Temperature Test", "Temperature Test"),
    ("Manual Test", "Manual Test"),
    ("LCD Check", "LCD Check"),
    ("Laser Alignment", "Laser Alignment"),
    ("Manual Test", "Manual Test"),
)

PRODUCT_STATUS = (
    ("ACTIVE", "ACTIVE"),
    ("INACTIVE", "INACTIVE"),
)

TEST_STATION = (
    ("CRICKET", "CRICKET"),
    ("FANJI", "FANJI"),
    ("BASS", "BASS"),
    ("CARP", "CARP"),
    ("BEIDOU", "BEIDOU"),
    ("72X", "72X"),
    ("HPUMP HTP", "HPUMP HTP"),
    ("5X", "5X"),
    ("TIC300", "TIC300"),
    ("LEPTON", "LEPTON"),
    ("ZULU", "ZULU"),
    ("SHAKA", "SHAKA"),
    ("PRO3000 PROBE", "PRO3000 PROBE"),
    ("PRO3000 TONER", "PRO3000 TONER"),
    ("INTELLITONE PROBE", "INTELLITONE PROBE"),
    ("INTELLITONE TONER", "INTELLITONE TONER"),
    ("MS2", "MS2"),
    ("MS-POE", "MS-POE"),
    ("WIREMAP", "WIREMAP"),
)

class cells_Name(models.Model):
    cell_Name = models.CharField(max_length=100, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cell_Name

class Sku_Info(models.Model):
    product_Status = models.CharField(max_length=20, choices=PRODUCT_STATUS, null=True)
    #test_Cells = models.CharField(max_length=20, choices=TEST_STATION, null=True)
    test_Cells = models.ForeignKey(cells_Name, on_delete=models.CASCADE, null=True)
    product_Model = models.CharField(max_length=100, null=True)
    FG_PartNo = models.CharField(max_length=100, null=True)
    FG_Model = models.CharField(max_length=100, null=True)
    #failure_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    PCA_SN_Number = models.CharField(max_length=100, null=True)
    #failure_Description = models.CharField(max_length=200, null=True)
    #failure_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.product_Model

#class getDebugData(forms.Form):
  #info = forms.CharField(max_length=100)
  #order_quantity = forms.IntegerField()
  #date = forms.DateTimeField()

class Failure_Mode(models.Model):
    test_Cells = models.ForeignKey(cells_Name, on_delete=models.CASCADE, null=True)
    test_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    failure_Mode = models.CharField(max_length=100, null=True)
    #order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.test_Station
        #return f"{self.info} ordered quantity {self.order_quantity}"
      
class Failure_Data(models.Model):
    test_Cells = models.ForeignKey(cells_Name, on_delete=models.CASCADE, null=True)
    test_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    failure_Mode = models.ForeignKey(Failure_Mode, on_delete=models.CASCADE, null=True)
    #order_quantity = models.PositiveIntegerField(null=True)
    date_Registered = models.DateTimeField(auto_now_add=True)
    find_items = models.Lookup

    def __str__(self) -> str:
        return self.test_Station
      