from django.urls import path
from .views import *

urlpatterns = [
    path('initiate_auth/', InitiateAuthView.as_view(),name='initiate_auth'),
    path('update_custom_field/', UpdateCustomFieldView.as_view(), name='update_custom_field'),

]
