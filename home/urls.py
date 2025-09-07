from django.urls import path
from . import views 
urlpatterns =[
  # the forst argument: empty quotes '' indicates that home is the root URL
  #Second argument: views,index indicates that the index function in the views file is responsible for processing that request
  # The third argument, name="home.index" is the name if the URL pattern
  path('', views.index, name='home.index'),
  path('about', views.about, name="home.about" )
]

"""Defining a view function

Django views are Python functions or classes that receive web requests and return web responses. They contain the logic to process HTTP requests and generate appropriate HTTP responses, typically in the form of HTML content to be rendered in the user’s web browser."""