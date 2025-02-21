from django.urls import path
from . import views

urlpatterns = [
    path('', views.shade_redesign, name='shade_redesign'),
    path('register/', views.register, name='register'),
    path('sa-pga-map/', views.sa_pga_map, name='sa_pga_map'), 
    path('contact-us/', views.contact_us, name='contact_us'),
    path('send_email/', views.send_email, name='send_email'),
    path('send_email_to_user/', views.send_email_to_user, name='send_email_to_user'),
    # Add more paths as needed
]
