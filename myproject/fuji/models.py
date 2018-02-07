from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    pn = models.CharField(max_length=18, unique=True)
    designChange = models.CharField(max_length=2, blank=False, null=True)
    partName = models.CharField(max_length=80, blank=False, null=True)
    partNamePort = models.CharField(max_length=80, blank=True, null=True)
    rating = models.CharField(max_length=80, blank=True, null=True)
    remark = models.CharField(max_length=80, blank=True, null=True)
    information = models.CharField(max_length=80, blank=True, null=True)
    yenPrice = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    ncm = models.CharField(max_length=8, blank=True, null=True)
    finalidade = models.CharField(max_length=500, blank=True, null=True)
    material = models.CharField(max_length=80, blank=True, null=True)
    comentarios = models.CharField(max_length=500, blank=True, null=True)
    updated_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+", null=True)

    def __str__(self):
        return self.pn