from django.urls import path
from vercel_app import api, page

# configuration --> boslife config
# subscription --> subscrib from this site
urlpatterns = [
    # index
    path('', page.index, name='index'),
    # api
    path('api/get_model_list', api.get_model_list, name='get_model_list'),
]

