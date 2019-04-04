import pyexcel as pe
import json
from django.shortcuts import render
from pyexcel.exceptions import FileTypeNotSupported

# Create your views here.


def upload(request):
    records=[]
    names=[]
    if request.method == 'POST' and 'excel' in request.FILES:
        try:
            filename = request.FILES['excel'].name
            extension = filename.split(".")[1]
            content = request.FILES['excel'].read()
            sheet = pe.get_sheet(
                file_type=extension,
                file_content=content,
                name_columns_by_row=0)
            names = sheet.colnames
            records = sheet.to_records
            # return render(request, 'ind.html', {'records': records, 'headers': names})
        except FileTypeNotSupported:
            return render(request, 'error-page.html')
    return render(request, 'upl.html', {'records': records, 'headers': names})
