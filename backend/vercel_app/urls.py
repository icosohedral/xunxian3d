from django.urls import path
from vercel_app import api

# configuration --> boslife config
# subscription --> subscrib from this site
urlpatterns = [
    # api
    path('api/get_model_list', api.get_model_list, name='get_model_list'),
]

