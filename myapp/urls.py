from django.urls import path
from myapp import views
urlpatterns = [
    
  
    path('selenium', views.timtruyen_selenium, name='timtruyen_selenium'),
    path('', views.nhapdata, name='nhapdata'),
]