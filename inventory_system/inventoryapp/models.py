# inventory/models.py
from email.policy import default
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django import forms
from django.db.models.signals import post_save
from django.dispatch import receiver

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

# User and adding One More Field (user_type)

class cells_Name(models.Model):
    id = models.AutoField(primary_key=True)
    cell_Name = models.CharField(max_length=100, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.cell_Name
      
class station_Name(models.Model):
    id = models.AutoField(primary_key=True)
    station_Name = models.CharField(max_length=100, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.station_Name
      
class model_Name(models.Model):
    id = models.AutoField(primary_key=True)
    model_Name = models.CharField(max_length=100, null=True)
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.model_Name

class Sku_Info(models.Model):
    id = models.AutoField(primary_key=True)
    product_Status = models.CharField(max_length=20, choices=PRODUCT_STATUS, null=True)
    #test_Cells = models.CharField(max_length=20, choices=TEST_STATION, null=True)
    test_Cells = models.CharField(max_length=100, null=True)
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
    id = models.AutoField(primary_key=True)
    test_Cells = models.CharField(max_length=100, null=True)
    test_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    failure_Mode = models.CharField(max_length=100, null=True)
    #order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.test_Station
        #return f"{self.info} ordered quantity {self.order_quantity}"
      
class Failure_Data(models.Model):
    id = models.AutoField(primary_key=True)
    test_Cells = models.ForeignKey(cells_Name, on_delete=models.CASCADE, null=True)
    test_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    failure_Mode = models.ForeignKey(Failure_Mode, on_delete=models.CASCADE, null=True)
    #order_quantity = models.PositiveIntegerField(null=True)
    date_Registered = models.DateTimeField(auto_now_add=True)
    find_items = models.Lookup

    def __str__(self) -> str:
        return self.test_Station

class CustomUser(AbstractUser):
    ADMIN = '1'
    ENGTECH = '2'
    OPERATOR = '3'
    
    EMAIL_TO_USER_TYPE_MAP = {
        'admin': ADMIN,
        'engtech': ENGTECH,
        'operator': OPERATOR
    }

    user_type_data = ((ADMIN, "ADMIN"), (ENGTECH, "ENGTECH"), (OPERATOR, "OPERATOR"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    
    
class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class engTech(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Operator(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(admin=instance)
        if instance.user_type == 2:
            engTech.objects.create(admin=instance)
        if instance.user_type == 3:
            Operator.objects.create(admin=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.engineer.save()
    if instance.user_type == 3:
        instance.operator.save()