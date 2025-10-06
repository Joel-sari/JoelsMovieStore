from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import Order, Item
from django.contrib.auth.decorators import login_required
import googlemaps
from django.conf import settings



#We define the add function, which takes two parameters: the request and the movie ID.
from movies.models import Movie
#We fetch the Movie object with the given id from the database (by using the get_object_or_404 function). If no such object is found, a 404 (Not Found) error is raised.
from .utils import calculate_cart_total
def index(request):
    cart_total = 0
    movies_in_cart = []
    cart = request.session.get('cart', {})
    #We initialize the cart_total to 0, and movies_in_cart as an empty list.
    #We retrieve the cart information from the session using request.session.get('cart', {}).
    movie_ids = list(cart.keys())

    #If there are any movie IDs in the cart, the function queries the database for movies with those IDs using Movie.objects.filter(id__in=movie_ids). Additionally, we calculate the total cost of the movies in the cart using the calculate_cart_total function, which updates the cart_total variable.
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    
    return render(request, 'cart/index.html',
        {'template_data': template_data})

def add(request, id):
    #We check the session storage for a key called 'cart'. If the key does not exist, a {} empty dictionary is assigned to the cart variable.
    get_object_or_404(Movie, id=id)
    cart = request.session.get('cart', {})

    #We modify the cart variable. We add a new key to the cart dictionary based on the movie ID, and the corresponding value based on the movie quantity the user wants to add to the cart (we will collect quantity through an HTML form later). For example, if the user wants to add 2 movies with id=1, a new key/value such as this cart["1"] = "2" will be added to the dictionary.

    cart[id] = request.POST['quantity']
    #The updated cart dictionary is then saved back to the session using request.session['cart'] = cart.
    request.session['cart'] = cart
    return redirect('cart.index')
def clear(request):
    request.session['cart'] = {}
    return redirect('cart.index')

@login_required
def purchase(request):

    #We use the login_required decorator to ensure that the user must be logged in to access the purchase function.
    #We define the purchase function, which will handle the purchase process.
    #We retrieve the cart data from the user’s session. The cart variable will contain a dictionary with movie IDs as keys and quantities as values.
    #We retrieve the movie IDs stored in the cart dict and convert them into a list named movie_ids.
    #We check if the movie_ids list is empty (which indicates the cart is empty). In this case, the user is redirected to the cart.index page (here, the purchase function finalizes its execution).
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids == []):
        return redirect('cart.index')
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    # Extract shipping details from the POST data submitted by the user
    city = request.POST.get('city', '')
    state = request.POST.get('state', '')
    country = request.POST.get('country', '')

    # Initialize Google Maps client with API key from settings
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

    # Combine city, state, and country into a full address string
    full_address = ', '.join(filter(None, [city, state, country]))

    # Geocode the full address to get latitude and longitude
    print("DEBUG full_address:", full_address)
    geocode_result = gmaps.geocode(full_address)
    print("DEBUG geocode_result:", geocode_result)

    # Create a new Order object and assign the user, total, and shipping details
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.city = city  # Assign the city from the shipping form to the order
    order.state = state  # Assign the state from the shipping form to the order
    order.country = country  # Assign the country from the shipping form to the order

    # If geocoding was successful, extract latitude and longitude and save to order
    if geocode_result:
        location = geocode_result[0]['geometry']['location']
        order.latitude = location.get('lat')
        order.longitude = location.get('lng')
        # Also capture the Google-verified formatted address for display
        formatted_address = geocode_result[0].get('formatted_address', '')

    order.save()
    print("DEBUG TEMPLATE LAT/LNG:", order.latitude, order.longitude)

    """If the cart is not empty, we continue the purchase process.
    We retrieve movie objects from the database based on the IDs stored in  the cart using Movie.objects.filter(id__in=movie_ids.
    We calculate the total cost of the movies in the cart using the calculate_cart_total() function.
    We create a new Order object. We set its attributes such as user (the logged-in user) and total (the cart total), and save it to the database.
    We iterate over the movies in the cart. We create an Item object for each movie in the cart. For each Item, we set its price and quantity, link the corresponding movie and order, and save it to the database."""

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
        

    """Lets analyze this piece of code:
    After the purchase is completed, we clear the cart in the users session by setting request.session['cart'] to an empty dictionary.
    We prepare the data to be sent to the purchase confirmation template. This data includes the title of the page and the ID of the created order.
    Finally, we render the cart/purchase.html template."""
    request.session['cart'] = {}
    template_data = {
        'title': 'Purchase confirmation',
        'order_id': order.id,
        'latitude': order.latitude,
        'longitude': order.longitude,
        # Add formatted address for display in confirmation template
        'formatted_address': formatted_address,
        "MAPS_JS_API_KEY": settings.MAPS_JS_API_KEY, 
        
    }
    print("DEBUG TEMPLATE DATA:", template_data)
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})

    
