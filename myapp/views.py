from django.shortcuts import render

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
# Add more views as needed
