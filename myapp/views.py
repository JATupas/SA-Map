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
      # Define the path to the CSV file
    csv_file_path = os.path.join(settings.BASE_DIR, 'myapp', 'data', 'points.csv')
    
    # Load the points and additional data from the CSV file
    df = pd.read_csv(csv_file_path)
    points = df[['xcoord', 'ycoord']].values
    values_sa1 = df['Combined-SA1'].values
    values_sa02 = df['Combined-SA02'].values
    values_tl = df['TL'].values
    
    sa1 = None
    sa02 = None
    tl = None
    given_point = None
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('lon'))
            given_point = [lat, lon]
            
            # Debugging information
            print("Received coordinates:", given_point)

            # Perform interpolation to find the nearest values
            interpolated_sa1 = griddata(points, values_sa1, given_point, method='linear')
            interpolated_sa02 = griddata(points, values_sa02, given_point, method='linear')
            interpolated_tl = griddata(points, values_tl, given_point, method='nearest')

            # Handle potential NaN values in interpolation results
            if np.isnan(interpolated_sa1):
                interpolated_sa1 = None
            if np.isnan(interpolated_sa02):
                interpolated_sa02 = None
            if np.isnan(interpolated_tl):
                interpolated_tl = None

            response_data = {
                'current_coord': given_point,
                'sa1': float(interpolated_sa1) if interpolated_sa1 is not None else None,
                'sa02': float(interpolated_sa02) if interpolated_sa02 is not None else None,
                'tl': float(interpolated_tl) if interpolated_tl is not None else None,
            }
            return JsonResponse(response_data)
        except Exception as e:
            print("Error processing coordinates:", str(e))
            return HttpResponseBadRequest("Invalid data")

    context = {
        'current_coord': given_point,
        'sa1': sa1,
        'sa02': sa02,
        'tl': tl,
    }
    return render(request, 'sa-pga-map.html', context)
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