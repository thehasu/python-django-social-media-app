from django.contrib import admin

from .models import City, Country, Profile

# Register your models here.

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Profile)
