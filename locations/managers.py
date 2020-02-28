from datetime import datetime

from django.db import models
from mtm.settings import URL_REGEX, HTTP_HTTPS_REGEX, PHONE_REGEX

class NeighborhoodManager(models.Manager):
    def create_neighborhood(self, name):
        return self.create(name=name)

    def autocomplete(self, request):
        from .models import Neighborhood

        query = request.GET.get('q', '')
        neighborhoods = []

        if query == '':
            return {'neighborhoods': []}

        for neighborhood in Neighborhood.objects.filter(name__icontains=query) \
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

    def autocomplete(self, request):
        from .models import Location

        query = request.GET.get('q', '')
        locations = []

        if query == '':
            return {'locations': []}

        for location in Location.objects.filter(name__icontains=query) \
        .order_by('name')[:5]:
            locations.append({
                'id': location.id,
                'name': location.name,
            })

        return {'locations': locations}

    def location(self, category_slug, location_name, location_id):
        from mtm.settings import TZ
        from .models import Location, CATEGORIES
        from events.models import Event

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return (False, {'status': 'invalid ID'})

        _category_slug = CATEGORIES[location.category]
        _location_name = location.slug

        if _category_slug != category_slug or _location_name != location_name:
            return (False, {
                'status': 'invalid slug',
                'args': [_category_slug, _location_name, location_id],
            })

        events = Event.objects.filter(
            location=location,
            date_start__gte=datetime.now(TZ).replace(
                hour=0, minute=0, second=0, microsecond=0),
        ).order_by('date_start')[:10]

        return (True, {
            'location': location,
            'events': events,
            'category_name': Location.CATEGORY_CHOICES[location.category][1],
            'category_slug': _category_slug,
            'no_kitchen': location.no_kitchen,
        })

    def update_location(self, request):
        from .models import Location, Neighborhood, CATEGORIES

        location_id = int(request.POST.get('id'))
        location_name = request.POST.get('location-name', '')
        category = int(request.POST.get('category'))
        neighborhood_id = int(request.POST.get('neighborhood-id'))
        neighborhood_name = request.POST.get('neighborhood-name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip-code')
        website = request.POST.get('website')
        phone = request.POST.get('phone')

        errors = []

        if not location_id:
            errors.append('Invalid location ID.')

        if not location_name:
            errors.append('Location name is required.')

        if not neighborhood_id and neighborhood_name:
            Neighborhood.objects.create_neighborhood(neighborhood_name)
        elif not neighborhood_id or not neighborhood_name:
            errors.append('Neighborhood name is required.')

        if not address1:
            errors.append('Address line 1 is required.')

        if not city:
            errors.append('City is required.')

        if not state:
            errors.append('State is required.')

        if website and not URL_REGEX.match(website):
            errors.append('Please enter a valid URL.')

            if not HTTP_HTTPS_REGEX.match(website):
                errors.append('URL must start with http:// or https://.')

        if phone:
            if not PHONE_REGEX.match(phone):
                errors.append('Please enter a 10-digit phone number.')
                errors.append('Suitable formats: 123-456-7890, (123) 456-7890, 123 456 7890, 123.456.7890, 1234567890')

            phone = PHONE_REGEX.sub(r'\2\3\4', phone)

        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            errors.append('The specified location could not be found.')

        if errors:
            return (False, {
                'errors': errors,
                'args': [
                    CATEGORIES[category],
                    location.slug,
                    location_id,
                ],
            })

        location.name = location_name
        location.category = category

        try:
            neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        except Neighborhood.DoesNotExist:
            try:
                neighborhood = Neighborhood.objects.get(name=neighborhood_name)
            except Neighborhood.DoesNotExist:
                neighborhood = Neighborhood.objects.create_neighborhood(neighborhood_name)

        location.neighborhood = neighborhood
        location.address1 = address1
        location.address2 = address2
        location.city = city
        location.state = state
        location.zip_code = zip_code
        location.website = website
        location.phone = phone

        location.save()

        return (True, {
            'success': 'You have successfully updated %s.' % location_name,
            'args': [
                CATEGORIES[category],
                location.slug,
                location_id,
            ],
        })
