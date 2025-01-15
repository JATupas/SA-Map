# Utility functions
import json
from django.http import JsonResponse

def extract_data(body, method):
    if method == "POST":
        try:
            data = json.loads(body)  # Parse JSON from the bodys
            return data
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)