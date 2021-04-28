from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Category)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
admin.site.register(Item)
admin.site.register(Contact)