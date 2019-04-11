import datetime
from django.contrib.auth.models import User
from django.db import models


class Row_id(models.Model):

    r_id = models.CharField(max_length=20, unique=True)
    r_date = models.DateField(blank=True, editable=False)
    r_time = models.TimeField(blank=True, editable=False)
    r_device = models.CharField(max_length=3, blank=True, editable=False)

    class Meta:
        ordering = ['r_id']

    def save(self, *args, **kwargs):
        save_date = datetime.datetime.strptime(self.r_id[3:11], '%d%m%Y')
        self.r_date = save_date.strftime('%Y-%m-%d')
        save_time = datetime.datetime.strptime(self.r_id[11:17], '%H%M%S')
        self.r_time = save_time.strftime('%H:%M:%S')
        self.r_device = self.r_id[-3:]
        super(Row_id, self).save(*args, **kwargs)

    def __str__(self):
        return self.r_id


class Batch_pr(models.Model):

    batch_name = models.CharField(max_length=20, unique=True)
    b_year = models.DecimalField(
        max_digits=1, decimal_places=0, blank=True, editable=False)
    b_month = models.CharField(max_length=1, blank=True, editable=False)
    b_number = models.DecimalField(
        max_digits=4, decimal_places=0, blank=True, editable=False)

    class Meta:
        ordering = ['b_year', 'b_month', 'b_number']

    def save(self, *args, **kwargs):
        self.b_year = self.batch_name[-1]
        self.b_month = self.batch_name[-2]
        self.b_number = self.batch_name[:-2]
        super(Batch_pr, self).save(*args, **kwargs)

    def __str__(self):
        return self.batch_name


class Raw_material(models.Model):

    code = models.CharField(max_length=6, unique=True)
    material_name = models.CharField(max_length=120)
    unit = models.CharField(max_length=3, default="кг")
    rate = models.IntegerField(default=1)
    barcode = models.CharField(
        max_length=13, unique=True, blank=True, null=True)

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


class Production2(models.Model):

    prod_batch = models.ForeignKey(Batch_pr, on_delete=models.CASCADE)
    prod_material = models.ForeignKey(Raw_material, on_delete=models.CASCADE)
    prod_decl_quantity = models.DecimalField(max_digits=7, decimal_places=3)
