# inventory/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from inventoryapp.models import failureInfo, getDebugData


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


class ProductForm(forms.ModelForm):
    class Meta:
        model = failureInfo
        fields = ["model", "failure_Station", "failure_Description"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = getDebugData
        fields = ["info", "order_quantity"]
