import requests
import pandas as pd
import json
from django.shortcuts import render
from django.views.generic.list import ListView
from django.db.models import Count, Min, Sum, Avg
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


def add_zero(q, v):
    for i in range(q-len(v)):
        v = "0"+v
    return v


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


class Varka_view(ListView):
    template_name = "listvar.html"

    def get_queryset(self, **kwargs):
        queryset = Production2.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        varka = "185D9"
        context = super(Varka_view, self).get_context_data(**kwargs)
        filter_set = self.get_queryset()
        # filter_set = filter_set.filter(prod_batch__batch_name=varka)
        rec = []
        for f in filter_set:
            qs = Weighting.objects.filter(
                batch__batch_name=f.prod_batch.batch_name,
                material__code=f.prod_material.code
            ).values('lot__lot_code').annotate(ss=Sum('quantity'))
            a = {
                'prod_batch': f.prod_batch.batch_name,
                'prod_material__code': f.prod_material.code,
                'prod_material__material_name': f.prod_material.material_name,
                'prod_decl_quantity': f.prod_decl_quantity,
                'www': qs,
                'lll': qs.count
            }
            rec.append(a)

        # f_set= filter_set.values('prod_material__code')

        # # ff_set=Weighting.objects.filter(batch__batch_name="100D9", material__code__in=f_set).annotate(ss=Sum('quantity'))
        # # fff_set =ff_set.values('material','lot').annotate(ss=Sum('quantity'))
        # filter_set = filter_set.filter(prod_batch__batch_name="100D9")
        # context['records2'] = f_set
        # f_obj=filter_set.values('prod_material__code','prod_material__material_name').annotate(tt=Sum('prod_decl_quantity'))
        # filter_set = filter_set.values('prod_batch','prod_material').annotate(tt=Sum('prod_decl_quantity'))
        # # filter_set = filter_set.filter(prod_batch__batch_name="101D9").annotate(tt=Sum('prod_decl_quantity'))
        # ff_set=Weighting.objects.filter(batch__batch_name="100D9").values('batch')
        # context['records3'] = filter_set
        context['records3'] = rec

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


def delete_prod(request):
    objs = Production2.objects.all()
    for obj in objs:
        obj.delete()
    return render(request, 'success-page.html')


def upload_simple_var(request):
    df_to_append = read_xl_file('static/var.xlsx')
    for index, row in df_to_append.iterrows():
        batch, _ = Batch_pr.objects.get_or_create(batch_name=row['batch'])
        try:
            material = Raw_material.objects.get(code=add_zero(6, row['code']))
        except Raw_material.DoesNotExist:
            material = Raw_material(code=add_zero(
                6, row['code']), material_name=row['name'])
            material.save()
        quantity = row['quant']
        new_prod_obj, _ = Production2.objects.get_or_create(
            prod_batch=batch,
            prod_material=material,
            prod_decl_quantity=quantity
        )
    return render(request, 'success-page.html')
