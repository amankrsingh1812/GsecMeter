from django.contrib import admin
from django.conf.urls import url
from . import views
from gsecWorkStatus import views
from django.urls import path
from  django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

app_name = 'candidate'



urlpatterns = [
    # url(r'^cultural/$', views.cultural, name='cultural'),
    url(r'^addagendaforgs/$', views.create_Agenda1, name='createagenda'),
    url(r'^home/$', views.home, name='vp'),
    url(r'^jugaad/(?P<pname>[\w\-]+)/$', views.jugaad, name='jugaad'),
    url(r'name/(?P<pname>[\w\-]+)/vote/$', views.vote, name='vote'),
    url(r'name/(?P<pname>[\w\-]+)/$',views.vp,name='gs'),
    url(r'^$', views.home, name='index'),
    # url(r'^technical/$', views.technical, name='technical'),
    # url(r'^welfare/$', views.welfare, name='welfare'),
    # url(r'^senator1/$', views.senator1, name='senator1'),
    # url(r'^hab/$', views.hab, name='hab'),
    # url(r'^sports/$', views.sports, name='sports'),
    url(r'^login/$',views.user_login,name='login'),
    url(r'^register/$',views.register,name='register'),
    url(r'^addagenda/$',views.addagenda,name='addagenda'),
    url(r'^verify/$',views.approvestatus,name='verify'),
    url(r'^verified/(?P<pk>[0-9]+)/$',views.verifysatus,name='verified'),
    url(r'^disapprove/(?P<pk2>[0-9]+)/$',views.disapprove,name='disapprove'),
     # url(r'^checkurl/$',views.checklogin(),name='checklogin'),
    url(r'^update/(?P<pk>[0-9]+)/$',login_required(views.UpdateAgenda.as_view()),name='updatestatus'),
    url(r'^comment/(?P<pk1>[0-9]+)/$',views.updatestatus,name='comment'),
    url(r'^logout/$',views.user_logout,name='logout'),
    url(r'^change_password/$',views.change_password,name='changepswd'),
    url(r'^compare/$',views.compare,name='compare'),
    url(r'^comparesenator/$',views.comparesenator,name='comparesenator'),
    url(r'^comparepast/$',views.comparepast,name='comparepast'
                                                 ''),

]