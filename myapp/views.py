
import os
import json
from django.conf import settings
import pandas as pd
from scipy.interpolate import griddata
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
import base64
from email.mime.image import MIMEImage
from django.core.mail import EmailMultiAlternatives
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import sys

def shade_redesign(request):
    return render(request, 'SHADE REDESIGN.html')

def contact_us(request):
    return render(request, 'contact-us.html')

from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        # Extract data from the form
        full_name = request.POST.get('full_name')
        birthdate = request.POST.get('birthdate')
        email = request.POST.get('email')
        profession = request.POST.get('profession')
        affiliation = request.POST.get('affiliation')

        # Validate required fields
        if not full_name or not email:
            return HttpResponseBadRequest("Full Name and Email are required.")

        # Save the data to the session
        request.session['registration_data'] = {
            'full_name': full_name,
            'birthdate': birthdate,
            'email': email,
            'profession': profession,
            'affiliation': affiliation,
        }

        # Redirect to the SA-PGA Map page
        return redirect('sa_pga_map')

    # For GET requests, render the registration form
    return render(request, 'register.html')




from .process.sapgamap import process_sa_pga_map  # Import the function from your external Python file

@csrf_exempt
def sa_pga_map(request):
    # Initialize values
    sa1, sa02, tl, Favalue, Fvvalue, SMS, SM1, SDS, SD1, Ts, To = [None] * 11
    given_point = None
    image_base64 = None
    registration_data = request.session.get('registration_data', None)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get latitude and longitude from the POST request
            lat_str = request.POST.get('lat')
            lon_str = request.POST.get('lon')
            site = request.POST.get('site')
            fainput = request.POST.get('fainput')
            fvinput = request.POST.get('fvinput')
            
            # Validate required fields
            if not lat_str or not lon_str or not site:
                return HttpResponseBadRequest("Missing required fields: latitude, longitude, and site.")
            
            # Convert strings to float
            lat = float(lat_str)
            lon = float(lon_str)
            fainput = float(fainput)
            fvinput = float(fvinput)
            
            # Log the received coordinates for debugging
            print(f"Received coordinates: lat={lat}, lon={lon}, site={site}, fa={fainput}, fv={fvinput}")
            
            # Process the map data using the given lat, lon
            response_data = process_sa_pga_map(lat, lon, site, fainput, fvinput)
            
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
        'registration_data': json.dumps(registration_data),
    }
    return render(request, 'sa-pga-map.html', context)

def send_email(request):
    if request.method == "POST":
        print(request.body)
        if request.body:
            try:
                # Parse JSON from the request body
                data = json.loads(request.body.decode('utf-8'))

                # image data

                image_data = base64.b64decode(data.get('calculationData', "").get("image_base64", ""))

                # Pass data to the template
                context = {
                    'data': data,
                    'has_data': True,
                    'cid': "ASCE-7_Spectral_Plot"
                }
            except json.JSONDecodeError:
                # Handle invalid JSON format
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        else:
            # Handle empty body
            context = {
                'data': None,
                'has_data': False
            }
        
        # Render html email template
        html_content = render_to_string('email-template.html', context)

        subject = "User Logs"  # changed to specific user name
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['shadelogs@gmail.com']

        email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")

        # Image Configuration
        img = MIMEImage(image_data)
        img.add_header('Content-ID', '<ASCE-7_Spectral_Plot>')  # Use the same CID as in the template
        img.add_header('Content-Disposition', 'inline', filename="ASCE-7 Spectral Plot.png")  # Add the filename
        email.attach(img)
        try:
            email.send()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        


def send_email_to_user(request):
    if request.method == "POST":
        if request.body:
            try:
                # Parse JSON from the request body
                data = json.loads(request.body.decode('utf-8'))

                # image data

                image_data = base64.b64decode(data.get('calculationData', "").get("image_base64", ""))
                user_email = data.get('registrationData','').get('email', '')

                # Pass data to the template
                context = {
                    'data': data,
                    'has_data': True,
                    'cid': "ASCE-7_Spectral_Plot"
                }
            except json.JSONDecodeError:
                # Handle invalid JSON format
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        else:
            # Handle empty body
            context = {
                'data': None,
                'has_data': False
            }
        
        # Render html email template
        html_content = render_to_string('user_email_template.html', context)

        subject = "Site Information"  # changed to specific user name
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]

        email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")

        # Image Configuration
        img = MIMEImage(image_data)
        img.add_header('Content-ID', '<ASCE-7_Spectral_Plot>')  # Use the same CID as in the template
        img.add_header('Content-Disposition', 'inline', filename="ASCE-7 Spectral Plot.png")  # Add the filename
        email.attach(img)
        try:
            email.send()
            return JsonResponse({'status': 'success', 'email': user_email})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
        

