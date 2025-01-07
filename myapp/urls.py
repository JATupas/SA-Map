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
    path('sa-pga-map/', views.sa_pga_map, name='sa_pga_map'), 
    # path('sa-pga-map/', views.sa_pga_map, name='sa_pga_map'),
    path('process_oq_jobs/', views.process_oq_jobs, name='process_oq_jobs'),

    path('calculate_occurrence_rates/', views.calculate_occurrence_rates, name='calculate_occurrence_rates'),
    path('catalog_declustering_tool/', views.catalog_declustering, name='catalog_declustering'),
    path('catalog_cleaning_tool/', views.clean_and_process_view, name='clean_and_process_data'),
    path('source_model_tool/', views.source_model, name='source_model'),
    path('recurrence_model_tool/', views.recurrence_model, name='recurrence_model'),
    path('send_email/', views.send_email, name='send_email')
    # Add more paths as needed
]
