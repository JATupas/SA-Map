import base64
import json
import numpy as np
import os
import pandas as pd
import sys
import weasyprint
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from email.mime.image import MIMEImage
from io import BytesIO
from scipy.interpolate import griddata
from weasyprint import HTML
from tempfile import NamedTemporaryFile

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
        
# def send_email_to_user(request):
#     if request.method == "POST":
#         if request.body:
#             try:
#                 # Parse JSON from the request body
#                 data = json.loads(request.body.decode('utf-8'))
#                 image_data = data.get('calculationData', {}).get("image_base64", "")
#                 user_email = data.get('registrationData', {}).get('email', '')

#                 # Decode Base64 image and save it as a temporary file
#                 if image_data:
#                     image_bytes = base64.b64decode(image_data)
#                     temp_img = NamedTemporaryFile(delete=False, suffix=".png", dir=settings.MEDIA_ROOT)
#                     temp_img.write(image_bytes)
#                     temp_img.close()
#                     image_path = temp_img.name
#                 else:
#                     image_path = None

#                 # Pass data to the template
#                 context = {
#                     'data': data,
#                     'has_data': True,
#                     'cid': "ASCE-7_Spectral_Plot",  # For email
#                     'image_base64': image_data,    # For email inline image
#                     'image_path': image_path       # For PDF image reference
#                 }

#             except json.JSONDecodeError:
#                 return JsonResponse({'error': 'Invalid JSON format'}, status=400)
#         else:
#             context = {
#                 'data': None,
#                 'has_data': False
#             }

#         # Render HTML email template
#         html_content = render_to_string('user_email_template.html', context)

#         # Render PDF with WeasyPrint using the image file path
#         if image_path:
#             pdf_html_content = render_to_string('user_pdf_template.html', context)
#             pdf_content = HTML(string=pdf_html_content, base_url=settings.MEDIA_ROOT).write_pdf()
#         else:
#             pdf_content = HTML(string=html_content).write_pdf()

#         # Subject and sender info
#         subject = "Site Information"
#         from_email = settings.DEFAULT_FROM_EMAIL
#         recipient_list = [user_email]

#         # Create email object
#         email = EmailMultiAlternatives(subject, '', from_email, recipient_list)
#         email.attach_alternative(html_content, "text/html")

#         # Attach the PDF
#         email.attach('Site_Info_Report.pdf', pdf_content, 'application/pdf')

#         try:
#             # Send the email
#             email.send()

#             # Clean up the temporary image file
#             if image_path:
#                 os.remove(image_path)

#             return JsonResponse({'status': 'success', 'email': user_email})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

def send_email_to_user(request):
    if request.method == "POST":
        try:
            # Extract JSON data from FormData
            registration_data = json.loads(request.POST.get("registrationData", "{}"))
            calculation_data = json.loads(request.POST.get("calculationData", "{}"))
            image_data = calculation_data.get("image_base64", "")
            user_email = registration_data.get("email", "")

            # Handle the uploaded file (map_snapshot.png)
            image_path = None
            if "imageFile" in request.FILES:
                image_file = request.FILES["imageFile"]
                temp_img = NamedTemporaryFile(delete=False, suffix=".png", dir=settings.MEDIA_ROOT)
                for chunk in image_file.chunks():
                    temp_img.write(chunk)
                temp_img.close()
                image_path = temp_img.name
                
            image_data_path = None
            if image_data:
                image_bytes = base64.b64decode(image_data)
                temp_img = NamedTemporaryFile(delete=False, suffix=".png", dir=settings.MEDIA_ROOT)
                temp_img.write(image_bytes)
                temp_img.close()
                image_data_path = temp_img.name
                

            # Static logo path
            static_logo_path = os.path.join(settings.BASE_DIR, "myapp", "static", "images", "shade_logo.png")
            home_icon_path = os.path.join(settings.BASE_DIR, "myapp", "static", "images", "Letterhead.svg")

            # Convert `HOME.png` to base64 for embedding in PDF
            home_icon_base64 = None
            if os.path.exists(home_icon_path):
                with open(home_icon_path, "rb") as home_icon_file:
                    home_icon_base64 = base64.b64encode(home_icon_file.read()).decode("utf-8")

            # Email context
            context = {
                "data": {
                    "registrationData": registration_data,
                    "calculationData": calculation_data
                },
                "has_data": True,
                "image_data_path": image_data_path,
                "image_path": image_path,
                "logo_cid": "shade_logo",
                "home_icon_base64": home_icon_base64,
            }

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        # Render email template
        html_content = render_to_string("user_email_template.html", context)

        # Modify PDF HTML to include embedded image (CID or base64)
        image_base64 = None
        if image_path:
            with open(image_path, "rb") as img_file:
                image_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        image_data_base64 = None
        if image_data_path:
            with open(image_data_path, "rb") as img_file:
                image_data_base64 = base64.b64encode(img_file.read()).decode("utf-8")

        # Render PDF content
        pdf_html_content = render_to_string("user_pdf_template.html", {
            **context,
            "image_base64": image_base64,  # Embed the main image as base64 into the PDF
            "image_data_base64": image_data_base64,  # Embed the additional base64 image into the PDF
        })

        pdf_content = HTML(string=pdf_html_content, base_url=settings.MEDIA_ROOT).write_pdf()


        # Create email object
        subject = "Site Information"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [user_email]
        email = EmailMultiAlternatives(subject, "", from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")

        # Attach PDF
        email.attach("Site_Info_Report.pdf", pdf_content, "application/pdf")

        # Attach static logo for email
        with open(static_logo_path, "rb") as logo_file:
            logo_attachment = MIMEImage(logo_file.read(), _subtype="png")
            logo_attachment.add_header("Content-ID", "<shade_logo>")
            logo_attachment.add_header("Content-Disposition", "inline", filename="shade_logo.png")
            email.attach(logo_attachment)

        try:
            print("Attempting to send email...")
            email.send()
            print("Email sent successfully.")

            # Clean up temporary image file
            if image_path:
                os.remove(image_path)
            if image_path:
                os.remove(image_data_path)

            return JsonResponse({"status": "success", "email": user_email})
        except Exception as e:
            print("Error while sending email:", str(e))
            return JsonResponse({"status": "error", "message": str(e)}, status=500)