from django.urls import path
from . import views

urlpatterns = [
    path('', views.shade_redesign, name='shade_redesign'),
    path('occurrence-rate-calculator/', views.occurrence_rate_calculator, name='occurrence_rate_calculator'),
    path('openquake-calculator/', views.openquake_calculator, name='openquake_calculator'),
    path('catalog-declustering-tool/', views.catalog_declustering_tool, name='catalog_declustering_tool'),
    path('earthquake-catalog-cleaner/', views.earthquake_catalog_cleaner, name='earthquake_catalog_cleaner'),
    path('recurrence-model-calculator/', views.recurrence_model_calculator, name='recurrence_model_calculator'),
    path('source-model-generator/', views.source_model_generator, name='source_model_generator'),
    # Add more paths as needed
]
