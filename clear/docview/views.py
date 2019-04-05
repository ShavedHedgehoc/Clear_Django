import requests
import json
from django.shortcuts import render
from django.views.generic.list import ListView
from .models import(
    Weighting,
    Row_id,
    Batch_pr,
    Raw_material,
    Lot,
    W_user,
)


def get_documents_list():
    response = requests.get(
        "http://srv-webts:9000/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=id")
    get_data = response.json()
    return get_data


def get_documents_quant():
    response = requests.get(
        "http://srv-webts:9000/MobileSMARTS/api/v1/Docs/Vzveshivanie?$select=none&$count=true")
    data = response.json()
    quant = data['@odata.count']
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
        context['files'] = get_documents_quant()
        return context