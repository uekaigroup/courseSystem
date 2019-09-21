from django.urls import path
from . import views

app_name='class'

urlpatterns = [
    path('', views.index,name='index'),
    path('getcourse/', views.getcourse,name='getcourse'),
    path('getteacher/<classname>/<newstage>', views.getteacher,name='getteacher'),
    path('getstage/<classname>', views.getstage,name='getstage'),
    path('getroom/<classname>', views.getroom,name='getroom'),
    path('savedata/', views.savedata,name='savedata'),
    path('getnext2course/<week>', views.getnext2course,name='getnext2course'),
]

