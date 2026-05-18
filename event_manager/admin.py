from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(EventManager)
admin.site.register(Event)
admin.site.register(Programme)
admin.site.register(Notification)
