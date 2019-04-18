from django.urls import path
from django.conf.urls import url
from .import views


urlpatterns = [ 
url(r'^docsup$', views.simple, name='simple'),
url(r'^delete$', views.delete_prod, name='simple'),
url(r'^loadvar$', views.upload_simple_var, name='simple'),
url(r'^docview$', views.Weighting_view.as_view(), name='ww'),
url(r'^batchview$', views.Batch_view.as_view(), name='ww'),
url(r'^varview$', views.Varka_view.as_view(), name='ww'),
]