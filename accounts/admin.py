from django.contrib import admin
from .models import Profile

# Custom admin configuration for the Profile model
class ProfileAdmin(admin.ModelAdmin):
    # list_display controls which fields show up in the Django admin list view
    # Here we show:
    # - user: the linked User model
    # - first_name: the user's first name stored in the Profile model
    # - last_name: the user's last name stored in the Profile model
    # - favorite_movie: the user's favorite movie, as stored in the Profile model
    # - security_question: the security question used for authentication
    # - security_answer: the user's answer to the security question
    list_display = ('user', 'first_name', 'last_name', 'favorite_movie', 'security_question', 'security_answer')

    # search_fields allows admin users to search Profile records
    # by username, first name, last name, or the security question text.
    # Note: "user__username" follows Django's relation lookup syntax
    # to search inside the related User model.
    search_fields = ('user__username', 'first_name', 'last_name', 'security_question')

# Register Profile model with the custom admin configuration
admin.site.register(Profile, ProfileAdmin)
