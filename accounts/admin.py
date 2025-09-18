from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'security_phrase', 'security_answer')
    search_fields = ('user__username', 'security_phrase')

admin.site.register(Profile, ProfileAdmin)
