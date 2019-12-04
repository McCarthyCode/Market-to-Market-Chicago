from django.contrib import admin
from django.utils import timezone
from mtm.settings import TIME_ZONE
from events.models import Location, Event

timezone.activate(TIME_ZONE)

admin.site.register(Location)
admin.site.register(Event)
