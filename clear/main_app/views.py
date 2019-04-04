import pandas as pd
import datetime
from django.shortcuts import render
from datetime import datetime as dt
from django.views.generic.list import ListView
from .models import Production, Batch, Marking
from .models import Apparatus, Container, Conveyor

# Create your views here.


class Prod_view(ListView):
    template_name = "index.html"
    # model = Production # Если раскомментить строчку, get_queryset не нужен
    # context_object_name = 'records'  # Имя переменной для передачи в шаблон

    def get_queryset(self, **kwargs):
        queryset = Production.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Prod_view, self).get_context_data(**kwargs)
        filter_set = self.get_queryset()
        if self.request.GET.get('date'):
            if self.request.GET.get('filter'):
                date = self.request.GET.get('date')
                filter_set = filter_set.filter(p_date=date)
                select_date = date
                context['select_date'] = select_date
            if self.request.GET.get('forward'):
                date = self.request.GET.get('date')
                filter_set = filter_set.filter(p_date=inc_date(date))
                select_date = inc_date(date)
                context['select_date'] = select_date
            if self.request.GET.get('backward'):
                date = self.request.GET.get('date')
                filter_set = filter_set.filter(p_date=dec_date(date))
                select_date = dec_date(date)
                context['select_date'] = select_date
        context['records'] = filter_set
        return context


def inc_date(date_str):
    curr_date = dt.strptime(date_str, '%Y-%m-%d')
    next_date = curr_date+datetime.timedelta(days=1)
    date = next_date.strftime('%Y-%m-%d')
    return date


def dec_date(date_str):
    curr_date = dt.strptime(date_str, '%Y-%m-%d')
    next_date = curr_date-datetime.timedelta(days=1)
    date = next_date.strftime('%Y-%m-%d')
    return date


def index(request):
    queryset = Production.objects.all()
    return render(request, 'index.html', {'records': queryset})


def get_cur_date():
    full_date = dt.now()
    short_date = full_date.strftime('%Y-%m-%d')
    return short_date

# def get_date(date_str):
#     """ Функция для преобразования даты из DataFrame(str).
#     Преобразует значаение вида "ГГГГ-ММ-ДД ЧЧ-ММ-СС"
#     в значение вида "ГГГГ-ММ-ДД" """
#     full_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
#     short_date = full_date.strftime('%Y-%m-%d')
#     return short_date


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
