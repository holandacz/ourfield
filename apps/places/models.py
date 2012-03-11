# -*- coding: utf-8 -*-
#import wingdbstub

from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from django.db import connection, transaction
from current_user import registration
from django_extensions.db.models import TimeStampedModel
from current_user.models import CurrentUserField
from core.models import MyModel
from markernos import PlaceMarkernos
from tastypie.models import create_api_key
import map.utils as mapUtils

models.signals.post_save.connect(create_api_key, sender=User)

class Place(MyModel):
    confirmed = models.BooleanField("Confirmed?",)
    territoryno = models.CharField("Territory No", max_length=6, null=True, blank=True, db_index=True, default="4-1-2")
    sortno = models.PositiveIntegerField("Sort No", null=True, default=0)
    blockno = models.CharField("Block No", max_length=32, null=True, blank=True)
    pointno = models.PositiveIntegerField("Point No", null=True, blank=True)
    markerno = models.PositiveIntegerField("Marker No", default=0, db_index=True)
    houseno = models.CharField("House No", max_length=32, null=True, blank=True)
    persons = models.TextField("Persons", null=True, blank=True)
    interestlevel = models.IntegerField("Interest Level", null=True, blank=True)
    actions = models.TextField("Actions", null=True, blank=True)
    notes = models.TextField("Notes", null=True, blank=True)
    description = models.CharField("Description", max_length=255, null=True, blank=True)
    languages = models.CharField("Description", max_length=255, null=True, blank=True, default="e:English\ns:Spanish\nch:Chinese\nf:French\ni:Italian\nx:German\n?:Other")

    name = models.CharField("Name", max_length=128, null=True, blank=True)

    placetype_id = models.IntegerField("Place Type ID", null=True, blank=True)
    sourcetype = models.CharField("Source Type", max_length=16, null=True, blank=True)
    source_id = models.IntegerField("Source ID", null=True, blank=True)
    geocoded = models.BooleanField("GeoCoded?", default=True )
    multiunit = models.BooleanField("MultiUnit?", )
    residential = models.BooleanField("Residential?", default=True )
    deleted = models.BooleanField("Deleted?", db_index=True)
    googlemapurl = models.CharField("Google Map URL", max_length=255, null=True, blank=True)
    point = models.PointField("LatLng", default='POINT(0 0)')

    owner =  CurrentUserField(blank=True, related_name = "flt_place_owner", default=1)
    modifier = CurrentUserField(blank=True, related_name = "flt_place_modifier", default=1)


    provinceno = models.PositiveIntegerField("Province No", null=True, blank=True)
    cantonno = models.PositiveIntegerField("Canton No", null=True, blank=True)
    districtno = models.PositiveIntegerField("District No", null=True, blank=True)

    directions = models.CharField("Directions", max_length=255, null=True, blank=True)
    districtname = models.CharField("District Name", max_length=32, null=True, blank=True)

    number = models.PositiveIntegerField("Number", null=True, blank=True)
    geo_name_id = models.PositiveIntegerField("GEO Name ID", null=True, blank=True)
    religiousaffiliation = models.CharField("Religious Affiliation", max_length=32, null=True, blank=True)

    postalcode = models.CharField("Zip Code", max_length=32, null=True, blank=True)

    noteshtml = models.TextField("Notes HTML", null=True, blank=True)

    objects = models.GeoManager()

    #p1 = Place.objects.get(id=3006)
    #p2 = Place.objects.get(id=3007)
    #p1.calcDistanceSquare(p2)
    def calcDistanceSquare(self, place):
        """calc distance squared to a place"""
        return (self.point[0] - place.point[0])**2 + (self.point[1] - place.point[1])**2

    # http://code.activestate.com/recipes/576779-calculating-distance-between-two-geographic-points/
    # http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def calcDistance(self, place):
        import math
        
        lat1 = self.point[0]
        lon1 = self.point[1]
        lat2 = place.point[0]
        lon2 = place.point[1]
        
        radius = 6371 # km
    
        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
    
        return d        


    #p1 = Place.objects.get(id=2950)
    #p1.findClosestPlace('4-1-2')
    #print p1.findClosestPlace('4-1-2')
    def findClosestPlace(self):
        """find closest place excluding self. Must be geocoded."""
        minDistance = 999999999999 # better way?
        places = Place.objects.filter(territoryno = self.territoryno).filter(geocoded=
        True).exclude(deleted=True)
        
        if self.id:
            places = places.exclude(id=self.id)
        
        # are there any 
        if len(places) < 2:
            return None
        
        closestPlace = None
        for place in places:
            distance = self.calcDistanceSquare(place)
            if distance < minDistance:
                minDistance = distance
                closestPlace = place
                
        return closestPlace
    
    # p1 = Place.objects.get(id=2957); p2 = p1.adjoiningPlace('before'); print p1.calcDirection(p2)
    # http://hoegners.de/Maxi/geo/geo.py
    # http://www.platoscave.net/blog/2009/oct/5/calculate-distance-latitude-longitude-python/
    # http://rosettacode.org/wiki/Box_the_compass#Python
    # http://www.movable-type.co.uk/scripts/latlong.html
    def calcDirection(self, place):
        from math import *

        direction_names = ["N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        directions_num = len(direction_names)
        directions_step = 360./directions_num

        lat1 = self.point[0]
        lon1 = self.point[1]
        lat2 = place.point[0]
        lon2 = place.point[1]

        dLon = lon2 - lon1
        y = sin(dLon) * cos(lat2)
        x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)
        

        index = int(round(degrees(atan2(y, x))/directions_step ))
        index %= directions_num
        return direction_names[index]


    # p1 = Place.objects.get(id=2957)
    # p1.adjoiningPlace()
    # p1.adjoiningPlace('before')
    def adjoiningPlace(self, adjoin = 'after'): 
        """return place adjoining before or after within territory"""
        markerno = self.markerno
        adjoiningMarkerno = self.markerno + 1 if adjoin == 'after' else self.markerno - 1
        places = Place.objects.filter(territoryno = self.territoryno).filter(markerno=adjoiningMarkerno)
        
        return places[0] if places else None

    def mostInLineWith(self, closestPlace, prevPlace, nextPlace):
        """Return the Place that is most in line with"""
        if mapUtils.mostInLineWith(self.point, closestPlace.point, prevPlace.point, nextPlace.point) == 'prevPt':
            return prevPlace
        else:
            return nextPlace
        
    def ParseDetails(self):
        from django.contrib.gis.geos import Point
        latitude = 0.0
        longitude = 0.0
        if self.googlemapurl:
            import re
            # look for ll=9.999107,-84.106216 like string for lat/long
            # http://maps.google.com/maps?hl=en&ll=10.001479,-84.134258&spn=0.001751,0.002682&t=h&vpsrc=6&z=19
            reobj = re.compile(r"[&;\?]ll=(?P<latitude>[\-0-9.]+),(?P<longitude>[\-0-9.]+)")
            match = reobj.search(self.googlemapurl)
            if match:
                latitude = float(match.group("latitude"))
                longitude = float(match.group("longitude"))

                from django.contrib.gis.geos import Point
                self.point = Point(latitude, longitude)

        self.point = Point(latitude, longitude)
        self.isgeocoded = True if (self.point.y and self.point.x) else False

    @property
    def full_name(self):
        ret = u'p'
        ret += str(self.id)
        if self.territoryno:
            ret += ' t'
            ret += self.territoryno
        if self.markerno:
            ret += ' m'
            ret += str(self.markerno)

        return ret

    class Meta:
        db_table = u'of_places'               
        #unique_together = ("boundary_type", "name", "number", "code"),
        verbose_name_plural = "places"
        permissions = (
            ('access_places','Access to Places'), 
        )
        
    def save(self, *args, **kw):
        #self.ParseDetails()
        self.geocoded = True if (self.point.y and self.point.x) else False
        
        # In order to handle renumbering of markerno's, I need to see if markno has changed.
        # If so, handle renumbering
        # kw['handleMarkernos'] is set in test to quickly clone Places. Do not want to process markernos
        if not 'handleMarkernos' in kw or kw['handleMarkernos']:
            isnew = True if not self.id else False
            placeMarkernos = PlaceMarkernos(self, isnew = isnew)
            placeMarkernos.handleChange()
            
        if 'handleMarkernos' in kw:
            del(kw['handleMarkernos']) # was just temp
            
        super(Place, self).save(*args, **kw)
        
    def delete(self, *args, **kw):
        # If so, handle renumbering
        # kw['handleMarkernos'] is set in test to quickly clone Places. Do not want to process markernos
        if not 'handleMarkernos' in kw or kw['handleMarkernos']:
            placeMarkernos = PlaceMarkernos(self, isdeleted = True)
            placeMarkernos.handleChange()
            
        if 'handleMarkernos' in kw:
            del(kw['handleMarkernos']) # was just temp
        
        super(Place, self).delete(*args, **kw)
        
        
    def type(self):
        return u'place'

    def __unicode__(self):
        return self.full_name

