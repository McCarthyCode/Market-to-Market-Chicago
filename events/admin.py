from django.contrib import admin
from django.utils import timezone
from mtm.settings import TIME_ZONE
from .models import Event, RecurringEvent

timezone.activate(TIME_ZONE)

admin.site.register(Event)
admin.site.register(RecurringEvent)
