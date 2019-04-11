import requests
import json
import pandas as pd
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import(
    Weighting,
    Row_id,
    Batch_pr,
    Raw_material,
    Lot,
    W_user,
    Production2

)


def get_documents_list():
    try:
        response = requests.get(
            "http://srv-webts:9000/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=id")
        get_data = response.json()
    except:
        pass
    return get_data


def get_documents_quant():
    try:
        response = requests.get(
            "http://srv-webts:9000/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=none&$count=true")
        data = response.json()
        quant = data['@odata.count']
    except:
        quant = "Server not found"
    return quant


def simple(request):
    records = []
    docs_list = get_documents_list()
    for one_doc in docs_list['value']:
        request_prefix = "http://srv-webts:9000/MobileSMARTS/api/v1/Docs/Vzveshivanie('"
        request_postfix = "')?$expand=currentItems"
        request_full = request_prefix+one_doc['id']+request_postfix
        doc = requests.get(request_full)
        doc_json = doc.json()
        for one_row in doc_json['currentItems']:
            s_weighting_id, _ = Row_id.objects.get_or_create(
                r_id=doc_json['ShtrihkodEmkosti']
            )
            s_batch, _ = Batch_pr.objects.get_or_create(
                batch_name=doc_json['Varka']
            )
            s_material, _ = Raw_material.objects.get_or_create(
                code=one_row['productId'],
                material_name=one_row['productName']
            )
            s_lot, _ = Lot.objects.get_or_create(
                lot_code=one_row['Partiya']
            )
            s_w_user, _ = W_user.objects.get_or_create(
                w_user_name=doc_json['Vypolnil']
            )
            s_quantity = one_row['currentQuantity']
            new_weighting_obj, _ = Weighting.objects.get_or_create(
                weighting_id=s_weighting_id,
                batch=s_batch,
                material=s_material,
                lot=s_lot,
                w_user=s_w_user,
                quantity=s_quantity
            )

    return render(request, 'success-page.html')


class Batch_view(ListView):
    template_name = "batch_view.html"

    def get_queryset(self, **kwargs):
        queryset = Batch_pr.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Batch_view, self).get_context_data(**kwargs)
        filter_set = self.get_queryset()
        context['records'] = filter_set
        return context


class Weighting_view(ListView):
    template_name = "listdocs.html"
    # model = Production # Если раскомментить строчку, get_queryset не нужен
    # context_object_name = 'records'  # Имя переменной для передачи в шаблон

    def get_queryset(self, **kwargs):
        queryset = Weighting.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(Weighting_view, self).get_context_data(**kwargs)
        filter_set = self.get_queryset()
        if self.request.GET.get('filter'):
            if self.request.GET.get('batch'):
                batch = self.request.GET.get('batch')
                context['batch'] = batch
                if self.request.GET.get('batch_ch'):
                    filter_set = filter_set.filter(batch__batch_name=batch)
                    context['batch_ch'] = True
            if self.request.GET.get('code'):
                code = self.request.GET.get('code')
                filter_set = filter_set.filter(
                    material__code=code)
            if self.request.GET.get('lot'):
                lot = self.request.GET.get('lot')
                filter_set = filter_set.filter(lot__lot_code=lot)

        context['records'] = filter_set
        context['files'] = get_documents_quant()

        return context


def read_xl_file(r_file):
    xl = pd.ExcelFile(r_file)
    sh = xl.sheet_names[0]
    r_df = pd.read_excel(xl, sheet_name=sh, dtype=str)
    return r_df


def upload_simple_var(request):
    df_to_append = read_xl_file('static/var.xlsx')
    for index, row in df_to_append.iterrows():
        batch, _ = Batch_pr.objects.get_or_create(batch_name=row['batch'])
        material, _ = Raw_material.objects.get_or_create(
            material_name=row['name'], code=row['code'])
        quantity = row['quant']
        new_prod_obj = Production2.objects.create(
            prod_batch=batch,
            prod_material=material,
            prod_decl_quantity=quantity
        )
    return render(request, 'success-page.html')
