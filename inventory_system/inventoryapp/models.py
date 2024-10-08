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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username


class failureInfo(models.Model):
    test_Cells = models.CharField(max_length=20, choices=TEST_STATION, null=True)
    model = models.CharField(max_length=100, null=True)
    failure_Station = models.CharField(max_length=20, choices=FAILURE_STATION, null=True)
    PCA_SN_Number = models.CharField(max_length=100, null=True)
    failure_Description = models.CharField(max_length=200, null=True)
    failure_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.model


class getDebugData(models.Model):
    info = models.ForeignKey(failureInfo, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.info} ordered quantity {self.order_quantity}"
