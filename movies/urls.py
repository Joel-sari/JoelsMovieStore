from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='movies.index'),
    #Notice the int:id is now the path, this is cause of the dynamic changing between the different movies
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),

]