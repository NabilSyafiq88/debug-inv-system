# inventory/models.py
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

TEST_STATION = (
    ("PCA Burn IN", "PCA Burn IN"),
    ("Calibration", "Calibration"),
    ("Final Test", "Final Test"),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_address = models.CharField(max_length=40, null=True)
    mobile = models.CharField(max_length=12, null=True)
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username


class failureInfo(models.Model):
    model = models.CharField(max_length=100, null=True)
    testStation = models.CharField(max_length=20, choices=TEST_STATION, null=True)
    quantity = models.PositiveIntegerField(null=True)
    failureDescription = models.CharField(max_length=200, null=True)
    faildate = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return self.model


class getDebugData(models.Model):
    info = models.ForeignKey(failureInfo, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, models.CASCADE, null=True)
    order_quantity = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.info} ordered quantity {self.order_quantity}"
