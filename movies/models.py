from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


#Movie class is inheriting from models.Model
class Movie(models.Model):
    # id is is an AutoField value that automatically increments its value for each new record that’s added to the database. The primary_key=True parameter specifies that this field is the primary key for the table, uniquely identifying each record.
    id = models.AutoField(primary_key=True)

    #This is a CharField value that represents a string field with a maximum length of 255 characters. It stores the name of the movie.
    name = models.CharField(max_length=255)

     #This is an IntegerField value that stores integer values. It represents the price of the movie.
    price = models.IntegerField()

    #This is a TextField value that represents a text field with no specified maximum length. It stores a textual description of the movie.
    description = models.TextField()

    #This is an ImageField value that stores image files. The upload_to parameter specifies the directory where uploaded images will be stored. In this case, uploaded images will be stored in the movie_images/ directory within the media directory of the Django project. The media directory is used to store user-uploaded files, such as images, documents, or other media files. This directory is specified in your Django project’s settings (we will configure it later in this chapter).
    image = models.ImageField(upload_to='movie_images/')


    #This is a special method in Python classes that returns a string representation of an object. It concatenates the movie’s id value (converted into a string) with a hyphen and the movie’s name. This method will be useful when we display movies in the Django admin panel later.
    def __str__(self):
        return str(self.id) + ' - ' + self.name

#We define a Python class named Review, which inherits from models.Model. This means that Review is a Django model class.
class Review(models.Model):
    #id is an AutoField, which automatically increments its value for each new record added to the database. The primary_key=True parameter specifies that this field is the primary key for the table, uniquely identifying each record.
    id = models.AutoField(primary_key=True)

    #comment is a CharField, which represents a string field with a maximum length of 255 characters. It stores the movie review text.
    comment = models.CharField(max_length=255)

    # rating is a PositiveSmallIntegerField that stores user ratings between 1 and 5.
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=1
    )

    #date is a DateTimeField , which is used for date and time data. The auto_now_add=True ensures that the date and time are automatically set to the current date and time when the review is created.
    date = models.DateTimeField(auto_now_add=True)

    #movie is a foreign key relationship to the Movie model. A review is associated with a movie. The on_delete parameter specifies how to handle the deletion of a movie that a review is associated with. In this case, on_delete=models.CASCADE means that if the related movie is deleted, the associated review will also be deleted.
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    
    #user is another foreign key relationship but to the User model. A review is associated with a user (the person who wrote the review). Similar to the movie attribute, on_delete=models.CASCADE specifies that if the related user is deleted, the associated review will also be deleted.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    class Meta:
        unique_together = ('user', 'movie')

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)  # short description of petition
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    VOTE_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
    ]
    vote = models.CharField(max_length=3, choices=VOTE_CHOICES)

    class Meta:
        unique_together = ("petition", "user")  # prevent duplicate voting

    def __str__(self):
        return f"{self.user.username} voted {'Yes' if self.vote else 'No'}"