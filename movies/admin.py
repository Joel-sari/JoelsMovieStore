from django.contrib import admin
from .models import Movie, Review, Petition, PetitionVote

# We created a MovieAdmin class that inherits from admin.ModelAdmin. This defines a custom admin class that allows you to customize the behavior of the admin interface for the Movie model.
class MovieAdmin(admin.ModelAdmin):
    #We set an ordering attribute. This attribute sets the default ordering of the movie objects in the admin interface. In our case, it specifies that the movies should be ordered by their name field.
    ordering = ['name']

    #We added a search_fields attribute that specifies that only the name field of the Movie model is searchable in the admin interface. This means that users can enter keywords into a search box provided by the admin interface, and Django will filter the list of movie objects
    search_fields = ['name']

#Finally, we registered the Movie model with the custom admin class, MovieAdmin. This tells Django to use the MovieAdmin class to customize the admin interface for the Movie model.
admin.site.register(Movie, MovieAdmin)

admin.site.register(Review)

admin.site.register(Petition)
admin.site.register(PetitionVote)
