# inventory/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inventoryapp.models import Sku_Info, Failure_Mode, Failure_Data


class UserRegistry(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class SkuForm(forms.ModelForm):
    class Meta:
        model = Sku_Info
        fields = ["test_Cells", "product_Model","FG_PartNo" ,"FG_Model", "PCA_SN_Number","product_Status"]


class FailureForm(forms.ModelForm):
    class Meta:
        model = Failure_Mode
        fields = ["test_Cells", "test_Station","failure_Mode"]

class FailureData(forms.ModelForm):
    class Meta:
        model = Failure_Data
        fields = ["test_Cells", "test_Station","failure_Mode"]