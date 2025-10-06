from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from .models import * 


class GeocodingView(View):
  template_name = "moviemaps/geocoding.html"

  def get(self, request, pk):
    location = Locations.objects.get(pk=pk)
    context = {
      'location': location
    }
    return render(request, self.template_name, context)

