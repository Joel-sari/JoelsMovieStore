from django.db import models
from django.contrib.auth.models import User
from movies.models import Movie

class Order(models.Model):
    
    # id: This is an AutoField, which automatically increments its value for each new record added to the database. The primary_key=True parameter specifies that this field is the primary key for the table, uniquely identifying each record.
    id = models.AutoField(primary_key=True)

    #total: This is a IntegerField, which represents the total amount of the order. It stores integer values.
    total = models.IntegerField()

    #date: This is a DateTimeField , which represents the date and time when the order was created. auto_now_add=True ensures that the date and time are automatically set to the current date and time when the order is created.
    date = models.DateTimeField(auto_now_add=True)

    #user: This is a foreign key relationship to the User model, which establishes a many-to-one relationship between orders and users. It means that each order is associated with a single user, and each user can have multiple orders. on_delete=models.CASCADE specifies that if the related user is deleted, the associated orders will also be deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.user.username
    
class Item(models.Model):
    #id: This is an AutoField, which automatically increments its value for each new record added to the database. The primary_key=True parameter specifies that this field is the primary key for the table, uniquely identifying each record.
    id = models.AutoField(primary_key=True)

    #price: This is an IntegerField, which represents the price at which the item was purchased.
    price = models.IntegerField()

    #quantity: This is an IntegerField, which represents the desired quantity of the item to purchase.
    quantity = models.IntegerField()

    #order: This is a foreign key relationship with the Order model, which defines a foreign key relating each item to a specific order.
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    #movie: This is a foreign key relationship with the Movie model, which defines a foreign key relating each item to a specific movie.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name