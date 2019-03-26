import pandas as pd
from django.shortcuts import render
from datetime import datetime
from django.views.generic.list import ListView
from .models import Production, Batch, Marking
from .models import Apparatus, Container, Conveyor

# Create your views here.


class Prod_view(ListView):
    pass


def index(request):
    queryset = Production.objects.all()
    return render(request, 'index.html', {'records': queryset})


def get_date(date_str):
    """ Функция для преобразования даты из DataFrame(str).
    Преобразует значаение вида "ГГГГ-ММ-ДД ЧЧ-ММ-СС"
    в значение вида "ГГГГ-ММ-ДД" """
    full_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    short_date = full_date.strftime('%Y-%m-%d')
    return short_date


def read_xl_file(r_file):
    xl = pd.ExcelFile(r_file)
    sh = xl.sheet_names[0]
    r_df = pd.read_excel(xl, sheet_name=sh, dtype=str)
    return r_df


def upload_simple(request):
    df_to_append = read_xl_file('static/brief.xls')
    for index, row in df_to_append.iterrows():
        marking, _ = Marking.objects.get_or_create(r_name=row['marking'])
        batch, _ = Batch.objects.get_or_create(r_name=row['batch'])
        apparatus, _ = Apparatus.objects.get_or_create(
            rd_name=row['apparatus'])
        container, _ = Container.objects.get_or_create(
            rd_name=row['container'])
        conveyor, _ = Conveyor.objects.get_or_create(
            rd_name=row['conveyor'])
        new_prod_obj = Production.objects.create(
            p_date=get_date(row['date']),
            p_marking=marking,
            p_batch=batch,
            p_apparatus=apparatus,
            p_container=container,
            p_conveyor=conveyor)
    return render(request, 'success-page.html')
