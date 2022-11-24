from django.urls import path
from sales.views import listcustomers

urlpatterns = [
    path('customers/',listcustomers),
]