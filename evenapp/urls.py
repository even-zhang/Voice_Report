from django.conf.urls import url

from evenapp import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]