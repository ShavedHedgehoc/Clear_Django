from django.shortcuts import render
import pyexcel as pe

# Create your views here.

def upload(request):
    if request.method == 'POST' and 'excel' in request.FILES:        
        filename = request.FILES['excel'].name
        extension = filename.split(".")[1]        
        content = request.FILES['excel'].read()
        # if sys.version_info[0] > 2:
        #     # in order to support python
        #     # have to decode bytes to str
        #     content = content.decode('utf-8')
        records = pe.get_records(file_type=extension, file_content=content)        
        return render(request, 'ind.html',{'records':records})   
    return render(request, 'upl.html')

