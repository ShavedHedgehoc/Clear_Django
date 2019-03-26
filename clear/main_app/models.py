from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Refer_descr(
        models.Model):  #Абстрактная модель справочника с полем описания
    rd_name = models.CharField(max_length=10, unique=True)
    rd_descr = models.CharField(max_length=100, blank=True)

    class Meta:
        abstract = True
        ordering = ['rd_name']

    def __str__(self):
        return self.rd_name


class Apparatus(Refer_descr):  # Экземпляр справочника аппаратов
    pass


class Conveyor(Refer_descr):  # Экземпляр справочника конвейеров
    pass


class Container(Refer_descr):  # Экземпляр справочника емкостей
    pass


class Refer(models.Model):  #Абстрактная модель справочника с одним полем
    r_name = models.CharField(max_length=20, unique=True)

    class Meta:
        abstract = True
        ordering = ['r_name']

    def __str__(self):
        return self.r_name


class Batch(Refer):  # Справочник партий
    pass


class Marking(Refer):  # Справочник артикулов
    pass


class Production(models.Model):  # Экземпляр строки таблицы сводки
    p_date = models.DateField()
    p_marking = models.ForeignKey(Marking, on_delete=models.CASCADE)
    p_batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    p_plant = models.CharField(max_length=1, blank=True)
    p_cancelled = models.BooleanField(default=False)
    p_plan = models.IntegerField(default=10000)
    p_apparatus = models.ForeignKey(Apparatus, on_delete=models.CASCADE)
    p_container = models.ForeignKey(Container, on_delete=models.CASCADE)
    p_conveyor = models.ForeignKey(Conveyor, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.p_date) + " " + str(self.p_batch) + " " + str(
            self.p_marking)


class Fix_time(
        models.Model):  # Абстрактная модель таблицы фиксирования времени
    f_row = models.OneToOneField(Production, on_delete=models.CASCADE)
    f_time = models.TimeField(auto_now_add=True)  #, blank=True)
    f_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return "[" + str(self.f_row) + "] (" + str(self.f_time) + ") " + str(
            self.f_user)


class App_time(Fix_time):
    pass


class Prod_time(Fix_time):
    pass


class Conv_time(Fix_time):
    pass


class Plug_time(Fix_time):
    pass


class Start_time(Fix_time):
    pass


class Supp_time(
        models.Model):  # Экземпляр строки таблицы предполагаемых событий
    prod_row = models.OneToOneField(Production, on_delete=models.CASCADE)
    s_time_a = models.TimeField(blank=True)
    s_time_p = models.TimeField(blank=True)

    def __str__(self):
        return str(self.prod_row) + " " + str(self.s_time_a) + " " + str(
            self.s_time_p)