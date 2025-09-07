from django import template
"""
We use the register = template.Library() code to create an instance of template.Library, which is used to register custom template tags and filters.

We use the @register.filter(name='get_quantity') decorator to register the get_cart_quantity function as a custom template filter named get_quantity. The name='get_quantity' argument specifies the name of the filter as it will be used in templates.

We define the get_cart_quantity function, which takes two arguments: the cart session dictionary, and the ID of the movie for which the quantity is needed.

We access the quantity value by using the cart dictionary and movie_id as the key. We convert movie_id to a string to ensure compatibility with the cart keys.
Finally, we return the corresponding quantity value."""
register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return cart[str(movie_id)]