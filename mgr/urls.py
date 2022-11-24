from django.urls import path
from mgr import customer

urlpatterns = [
    path('customers',customer.dispatcher),
]