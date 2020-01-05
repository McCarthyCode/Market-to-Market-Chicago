from datetime import datetime

from django.db import models

class NeighborhoodManager(models.Manager):
    def create_neighborhood(self, name):
        return self.create(name=name)

    def neighborhoods_autocomplete(self, request):
        from .models import Neighborhood

        query = request.GET.get('q', '')
        neighborhoods = []

        if query == '':
            return {'neighborhoods': []}

        for neighborhood in Neighborhood.objects.filter(name__contains=query) \
        .order_by('name')[:5]:
            neighborhoods.append({
                'id': neighborhood.id,
                'name': neighborhood.name,
            })

        return {'neighborhoods': neighborhoods}

class LocationManager(models.Manager):
    def create_location(self, name, category, address1, address2='', city='Chicago', state='IL'):
        if address2:
            return self.create(name=name, category=category, address1=address1, address2=address2, city=city, state=state)
        else:
            return self.create(name=name, category=category, address1=address1, city=city, state=state)

    def locations_autocomplete(self, request):
        from .models import Location

        query = request.GET.get('q', '')
        locations = []

        if query == '':
            return {'locations': []}

        for location in Location.objects.filter(name__contains=query) \
        .order_by('name')[:5]:
            locations.append({
                'id': location.id,
                'name': location.name,
            })

        return {'locations': locations}

    def location(self, category, location_name, location_id):
        from mtm.settings import TZ
        from .models import Location, CATEGORIES
        from events.models import Event

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return (False, {'status': 'invalid ID'})

        _category = CATEGORIES[location.category]
        _location_name = location.slug

        if _category != category or _location_name != location_name:
            return (False, {
                'status': 'invalid slug',
                'args': [_category, _location_name, location_id],
            })

        events = Event.objects.filter(
            location=location,
            date_start__gte=datetime.now(TZ).replace(
                hour=0, minute=0, second=0, microsecond=0),
        ).order_by('date_start')[:10]

        return (True, {
            'location': location,
            'events': events,
            'category': _category,
        })
