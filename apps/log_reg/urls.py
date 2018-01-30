from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^logout$', views.logout),
    url(r'^show/(?P<id>\d+)$', views.show),
    url(r'^add/(?P<id>\d+)$', views.add_wish),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^add$', views.add),
    url(r'^additem$', views.additem),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
    url(r'^$', views.index)
]
