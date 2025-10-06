from django.urls import path
from .views import *

app_name = 'moviemaps'
urlpatterns = [
    path('geocoding/<int:pk>/', GeocodingView.as_view(), name='geocode'),
    path('', lambda request: render(request, 'moviemaps/geocoding_home.html'), name='map_home'),
]