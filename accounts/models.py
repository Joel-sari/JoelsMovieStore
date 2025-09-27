from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    # Standard, pre-defined security questions
    SECURITY_QUESTION_CHOICES = [
        ("fav_color", "What is your favorite color?"),
        ("first_pet", "What was the name of your first pet?"),
        ("birth_city", "In what city were you born?"),
        ("best_friend", "What is the first name of your best friend in high school?"),
        ("mother_maiden", "What is your mother’s maiden name?"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Optional personal details (kept on Profile to avoid touching the built-in User for now)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    favorite_movie = models.CharField(max_length=255, blank=True, null=True)

    # Security: use a select list of questions (phrase) + user-provided answer
    security_question = models.CharField(
        max_length=50, choices=SECURITY_QUESTION_CHOICES, blank=True, null=True
    )
    security_answer = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s profile"