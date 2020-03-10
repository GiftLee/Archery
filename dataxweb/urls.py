from django.urls import path
from dataxweb import views

urlpatterns = [
    path('dataxjoblist/', views.dataxJoblist),
    #path('dataxjobdetail/', views.dataxJobDetail),
    path('adddataxjob/', views.addDataxJob),
]