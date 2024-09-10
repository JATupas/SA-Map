import os
import json
from django.conf import settings
import pandas as pd
from scipy.interpolate import griddata
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
import numpy as np

def shade_redesign(request):
    return render(request, 'SHADE REDESIGN.html')

def occurrence_rate_calculator(request):
    return render(request, 'occurrence-rate-calculator.html')

def openquake_calculator(request):
    return render(request, 'openquake-calculator.html')

def catalog_declustering_tool(request):
    return render(request, 'catalog-declustering-tool.html')

def earthquake_catalog_cleaner(request):
    return render(request, 'earthquake-catalog-cleaner.html')

def recurrence_model_calculator(request):
    return render(request, 'recurrence-model-calculator.html')

def source_model_generator(request):
    return render(request, 'source-model-generator.html')

def sa_pga_map(request):
    return render(request, 'sa-pga-map.html')
# Add more views as needed

from .process.OQ_Run import run_oq_jobs
# from django.views.decorators.csrf import csrf_exempt

def process_oq_jobs(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        file_path = data.get('file_path')

        if file_path:
            try:
                # Run your function
                run_oq_jobs(file_path)
                return JsonResponse({'status': 'success', 'message': 'OQ Jobs started successfully'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file path provided'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from .process.occurence_rate import OCR_calc

def calculate_occurrence_rates(request):
    if request.method == "POST":
        input_file_path = request.POST.get('input_file_path')
        output_file_path = request.POST.get('output_file_path')

        try:
            OCR_calc(input_file_path, output_file_path, bin_width=0.1)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})

from .process.declustering import decluster_catalogue

def catalog_declustering(request):
    if request.method == "POST":
        input_file_path = request.POST.get('input_file_path')
        declustering_method = request.POST.get('declustering_method')
        time_method = request.POST.get('time_method')
        output_file_path = request.POST.get('output_file_path')
        try:
            decluster_catalogue(input_file_path, output_file_path, declustering_method, time_method)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})

from .process.data_processing_module import clean_and_process_data

def clean_and_process_view(request):
    if request.method == "POST":
        input_file_path = request.POST.get('input_file_path')
        output_file_path = request.POST.get('output_file_path')
        try:
            clean_and_process_data(input_file_path, output_file_path)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})

from .process.sourceModel_Generator import create_model

def source_model(request):
    if request.method == "POST":
        fault_file_path = request.POST.get('fault_file_path')
        earthquake_file_path = request.POST.get('earthquake_file_path')
        vertice_file_path = request.POST.get('vertice_file_path')
        output_file_path = request.POST.get('output_file_path')
        try:
            create_model(output_file_path, fault_file_path, earthquake_file_path, vertice_file_path)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})

from .process.GRLoop import analyze_faults

def recurrence_model(request):
    if request.method == "POST":
        fault_file_path = request.POST.get('fault_file_path')
        earthquake_file_path = request.POST.get('earthquake_file_path')
        vertice_file_path = request.POST.get('vertice_file_path')
        buffer_size = int(request.POST.get('buffer_size'))
        output_file_path = request.POST.get('output_file_path')
        gr_output_file_path = request.POST.get('gr_output_file_path')
        try:
            analyze_faults(output_file_path, gr_output_file_path, fault_file_path, earthquake_file_path, vertice_file_path, buffer_size)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'invalid request'})