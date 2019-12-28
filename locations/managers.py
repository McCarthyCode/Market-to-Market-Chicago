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
