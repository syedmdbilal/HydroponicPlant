from django.conf.urls import url
from employee import views

urlpatterns = [
    url('nail', views.nail, name='nail'),
]
