from django.contrib import admin
from .models import Beer
from .models import Brewery
from .models import Geocode

# Register your models here.

admin.site.register(Beer)
admin.site.register(Brewery)
admin.site.register(Geocode)
