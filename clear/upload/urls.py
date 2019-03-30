from django.urls import path
from django.conf.urls import url
from . import views as upload_views


urlpatterns = [ 
url(r'^up$', upload_views.upload, name='upload'),
]