from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.conf import settings
import os, json
    
def get_model_list(request):
    # static path
    data = []
    file_types = ['.obj', '.glb', '.gltf']
    model_path = os.path.join(settings.STATICFILES_DIRS[0], 'models')
    for file in os.listdir(model_path):
        for file_type in file_types:
            if file_type in file:
                data.append(file)
    return JsonResponse({'result': True, 'data': data, 'err': ''})
    

