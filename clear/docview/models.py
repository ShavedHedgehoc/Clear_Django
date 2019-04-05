from django.contrib.auth.models import User
from django.db import models


class Row_id(models.Model):
    """Дата-время-терминал, добавлять поля переопределением метода записи"""
    r_id = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['r_id']

    def __str__(self):
        return self.r_id


class Batch_pr(models.Model):
    batch_name = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['batch_name']

    def __str__(self):
        return self.batch_name


class Raw_material(models.Model):
    code = models.CharField(max_length=6, unique=True)
    material_name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['material_name']

    def __str__(self):
        return self.code + " " + self.material_name


class Lot(models.Model):
    lot_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.lot_code


class W_user(models.Model):
    w_user_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.w_user_name


class Weighting(models.Model):
    weighting_id = models.ForeignKey(Row_id, on_delete=models.CASCADE)
    batch = models.ForeignKey(Batch_pr, on_delete=models.CASCADE)
    material = models.ForeignKey(Raw_material, on_delete=models.CASCADE)
    lot = models.ForeignKey(Lot, on_delete=models.CASCADE)
    w_user = models.ForeignKey(W_user, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=7, decimal_places=3)

    class Meta:
        ordering = ['batch', 'material']

    def __str__(self):
        return str(self.weighting_id)+" "+str(self.batch)+" " +\
            str(self.material)+" "+str(self.lot)+" " + \
            str(self.w_user)+" "+str(self.quantity)
