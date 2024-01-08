from django.urls import path
from myapp import views
urlpatterns = [
    
  
    path('', views.timtruyen_selenium, name='timtruyen_selenium'),
]