from django.urls import path
from dataxweb import views

urlpatterns = [
    path('dataxjoblist/', views.dataxJoblist),
    path('savedataxjob/', views.saveDataxJob),
    path('dataxjob/', views.dataxJob),
    path('adddataxjob/', views.addDataxJob),
    
]