from django.urls import path
from dataxweb import views

urlpatterns = [
    path('dataxjoblist/', views.dataxJoblist),
    #path('dataxjobdetail/', views.dataxJobDetail),
    path('dataxjob/', views.dataxJob),
    path('adddataxjob/', views.addDataxJob),
]