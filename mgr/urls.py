from django.urls import path
from mgr import customer,sigin_in_out,medicine

urlpatterns = [
    path('customers',customer.dispatcher),
    path('signin',sigin_in_out.signin),
    path('signin',sigin_in_out.signout),
path('medicines',medicine.dispatcher),
]
