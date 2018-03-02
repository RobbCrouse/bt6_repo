from django.conf.urls import url
from . import views

urlpatterns = [
    #routes that render
    url(r'^success$', views.success),
    url(r'^users/(?P<id>\d+)$', views.detail),
    url(r'^ideaDetail/(?P<id>\d+)$', views.ideaDetail),


    #routes that redirect
    url(r'^createIdea$', views.createIdea),
    url(r'^favorite/(?P<id>\d+)$', views.favorite),
    url(r'^remove/(?P<id>\d+)$', views.remove),
]