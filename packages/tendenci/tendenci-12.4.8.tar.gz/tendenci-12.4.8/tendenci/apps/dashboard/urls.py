from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.new, name="dashboard"),
    url(r'^new/$', views.new, name="dashboard-new"),
    url(r'^old/$', views.index, name="dashboard-old"),
    url(r'^customize/$', views.customize, name="dashboard_customize"),
]
