from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review
from django.contrib.auth.decorators import login_required


"""Now, it will retrieve all movies if the search parameter is not sent in the current request, or it will retrieve specific movies based on the search parameter. Let’s explain the previous code."""
def index(request):
    #We retrieve the value of the search parameter by using the request.GET.get('search') method and assign that value to the search_term variable. Here, we capture the search input value submitted through the form defined in the previous section.
    search_term = request.GET.get('search')

    #f search_term is not empty, we filter movies where the name contains search_term. The __icontains lookup is used for a case-insensitive containment search.
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        #If search_term is empty, we retrieve all movies from the database without applying any filters.
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    

    # We collect all movies from the database by using the Movie.objects.all() method. Movie.objects is a manager in Django that serves as the default interface to query the database table associated with the model. It provides various methods to perform database operations such as creating, updating, deleting, and retrieving objects. The all() method fetches all objects from the database table represented by the model. Remember that we previously collected the movie information by using the movies variable; now, we use the Movie Django model.
    template_data['movies'] = movies

    
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    # We use the Movie.objects.get(id=id) method to retrieve a specific movie BASED ON ITS ID. Remember that id is passed by the URL and received as a parameter in the show function.
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}


    # We now access movie.name as an OBJECT ATTRIBUTE. Previously, we accessed the name as a key (movie['name']), since the dummy data variable stored dictionaries.
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews

    return render(request, 'movies/show.html',
                  {'template_data': template_data})

 #We import login_required, which is used to verify that only logged users can access the create_review function. If a guest user attempts to access this function via the corresponding URL, they will be redirected to the login page.
@login_required
def create_review(request, id):
    #The create_review takes two arguments: the request that contains information about the HTTP request, and the id, which represents the ID of the movie for which a review is being created. 
    # Then, we check whether the request method is POST and the comment field in the request’s POST data is not empty. If that is TRUE, the following happens:
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()

        #e set the review properties as follows:
        # We set the comment based on the comments collected in the form
        # We set the movie, based on the retrieved movie from the database
        # We set the user, based on the authenticated user who submitted the form
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    #We retrieve the Review object with the given review_id. If the review does not exist, a 404 error will be raised.
    review = get_object_or_404(Review, id=review_id)

    #We check whether the current user (request.user) is the owner of the review to be edited (review.user). If the user does not own the review, the function redirects them to the movie.show page.
    if request.user != review.user:
        return redirect('movies.show', id=id)
    #Then, we check whether the request method is GET. In that case, the function prepares data for the template and renders the edit_review.html template
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    #If the request method is POST and the comment field in the request’s POST data is not empty, the function proceeds to update the review and redirects the user to the movie show page.
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)



@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)