import os
import json
from django.conf import settings
import pandas as pd
from scipy.interpolate import griddata
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import sys

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


from .process.sapgamap import process_sa_pga_map  # Import the function from your external Python file

@csrf_exempt
def sa_pga_map(request):
    # Initialize values
    sa1, sa02, tl, Favalue, Fvvalue, SMS, SM1, SDS, SD1, Ts, To = [None] * 11
    given_point = None
    image_base64 = None

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get latitude and longitude from the POST request
            lat = float(request.POST.get('lat'))
            lon = float(request.POST.get('lon'))
            site = request.POST.get('site')
            
            # Log the received coordinates for debugging
            print(f"Received coordinates: lat={lat}, lon={lon}, site={site}")
            
            # Process the map data using the given lat, lon
            response_data = process_sa_pga_map(lat, lon, site)
            
            # Log the response data for debugging
            print(f"Response data: {response_data}")
            
            # Check if response_data is valid
            if not response_data:
                raise ValueError("No data returned from process_sa_pga_map")
            
            # Extract values from the response data
            image_base64 = response_data.get('image_base64')
            sa1 = response_data.get('sa1')
            sa02 = response_data.get('sa02')
            tl = response_data.get('tl')
            Favalue = response_data.get('Fa')
            Fvvalue = response_data.get('Fv')
            SMS = response_data.get('SMS')
            SM1 = response_data.get('SM1')
            SDS = response_data.get('SDS')
            SD1 = response_data.get('SD1')
            Ts = response_data.get('Ts')
            To = response_data.get('To')
            given_point = response_data.get('current_coord')
            
            # Return the processed data as a JSON response
            return JsonResponse({
                'current_coord': given_point,
                'sa1': float(sa1) if sa1 is not None else None,
                'sa02': float(sa02) if sa02 is not None else None,
                'tl': float(tl) if tl is not None else None,
                'Fa': float(Favalue) if Favalue is not None else None,
                'Fv': float(Fvvalue) if Fvvalue is not None else None,
                'SMS': float(SMS) if SMS is not None else None,
                'SM1': float(SM1) if SM1 is not None else None,
                'SDS': float(SDS) if SDS is not None else None,
                'SD1': float(SD1) if SD1 is not None else None,
                'Ts': float(Ts) if Ts is not None else None,
                'To': float(To) if To is not None else None,
                'image_base64': image_base64,
            })
        except Exception as e:
            print(f"Error processing coordinates: {str(e)}")  # More detailed logging
            return HttpResponseBadRequest("Invalid data")
    
    # For the initial page load (GET request)
    context = {
        'current_coord': given_point,
        'sa1': sa1,
        'sa02': sa02,
        'tl': tl,
        'Favalue': Favalue,
        'Fvvalue': Fvvalue,
        'SMS': SMS,
        'SM1': SM1,
        'SDS': SDS,
        'SD1': SD1,
        'Ts': Ts,
        'To': To,
    }
    return render(request, 'sa-pga-map.html', context)


# from .process.sapgamap import process_sa_pga_map

# def sa_pga_map(request):
#     # Initialize values
#     sa1, sa02, tl, Favalue, Fvvalue, SMS, SM1, SDS, SD1, Ts, To = [None] * 11
#     given_point = None
    
#     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         try:
#             # Get latitude and longitude from the POST request
#             lat = float(request.POST.get('lat'))
#             lon = float(request.POST.get('lon'))
            
#             # Process the map data using the given lat, lon
#             response_data = process_sa_pga_map(lat, lon)
            
#             # Extract values from the response data and include them
#             sa1 = response_data.get('sa1')
#             sa02 = response_data.get('sa02')
#             tl = response_data.get('tl')
#             Favalue = response_data.get('Fa')
#             Fvvalue = response_data.get('Fv')
#             SMS = response_data.get('SMS')
#             SM1 = response_data.get('SM1')
#             SDS = response_data.get('SDS')
#             SD1 = response_data.get('SD1')
#             Ts = response_data.get('Ts')
#             To = response_data.get('To')
#             given_point = response_data.get('current_coord')
            
#             # Prepare the response data for the client-side AJAX request
#             return JsonResponse({
#                 'current_coord': given_point,
#                 'sa1': float(sa1) if sa1 is not None else None,
#                 'sa02': float(sa02) if sa02 is not None else None,
#                 'tl': float(tl) if tl is not None else None,
#                 'Fa': float(Favalue) if Favalue is not None else None,
#                 'Fv': float(Fvvalue) if Fvvalue is not None else None,
#                 'SMS': float(SMS) if SMS is not None else None,
#                 'SM1': float(SM1) if SM1 is not None else None,
#                 'SDS': float(SDS) if SDS is not None else None,
#                 'SD1': float(SD1) if SD1 is not None else None,
#                 'Ts': float(Ts) if Ts is not None else None,
#                 'To': float(To) if To is not None else None,
#             })
#         except Exception as e:
#             print("Error processing coordinates:", str(e))
#             return HttpResponseBadRequest("Invalid data")

#     # If it's a GET request, return the initial context for rendering
#     context = {
#         'current_coord': given_point,
#         'sa1': sa1,
#         'sa02': sa02,
#         'tl': tl,
#         'Favalue': Favalue,
#         'Fvvalue': Fvvalue,
#         'SMS': SMS,
#         'SM1': SM1,
#         'SDS': SDS,
#         'SD1': SD1,
#         'Ts': Ts,
#         'To': To,
#     }
#     return render(request, 'sa-pga-map.html', context)

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