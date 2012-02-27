# -*- coding: utf-8 -*-
#import wingdbstub
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from current_user import registration
from django_extensions.db.models import TimeStampedModel
from current_user.models import CurrentUserField
from core.models import MyModel
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class Place(MyModel):
    confirmed = models.BooleanField("Confirmed?",)
    territoryno = models.CharField("Territory No", max_length=6, null=True, blank=True)
    sortno = models.PositiveIntegerField("Sort No", null=True, default=0)
    blockno = models.CharField("Block No", max_length=32, null=True, blank=True)
    pointno = models.PositiveIntegerField("Point No", null=True, blank=True)
    houseno = models.CharField("House No", max_length=32, null=True, blank=True)
    persons = models.TextField("Persons", null=True, blank=True)
    interestlevel = models.IntegerField("Interest Level", null=True, blank=True)
    actions = models.TextField("Actions", null=True, blank=True)
    notes = models.TextField("Notes", null=True, blank=True)
    description = models.CharField("Description", max_length=255, null=True, blank=True)

    name = models.CharField("Name", max_length=128, null=True, blank=True)

    placetype_id = models.IntegerField("Place Type ID", null=True, blank=True)
    sourcetype = models.CharField("Source Type", max_length=16, null=True, blank=True)
    source_id = models.IntegerField("Source ID", null=True, blank=True)
    geocoded = models.BooleanField("GeoCoded?", )
    multiunit = models.BooleanField("MultiUnit?", )
    residential = models.BooleanField("Residential?", default=True )
    deleted = models.BooleanField("Deleted?",)
    googlemapurl = models.CharField("Google Map URL", max_length=255, blank=True)
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
        if self.provinceno:
            ret += ' t'
            ret += str(self.provinceno).zfill(3) 
            ret += '-'
        if self.cantonno: # canton
            ret += str(self.cantonno).zfill(2) 
            ret += '-'
        if self.districtno:
            ret += str(self.districtno).zfill(3)
        if self.districtname:
            ret += ' '
            ret += self.districtname
        if self.territoryno:
            ret += '-'
            ret += self.territoryno
        if self.sortno:
            ret += ' '
            ret += str(self.sortno).zfill(4)
        if self.blockno:
            ret += ' b'
            ret += str(self.blockno).zfill(3)
        if self.pointno:
            ret += ' p'
            ret += str(self.pointno).zfill(2)

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
        super(Place, self).save(*args, **kw)

    def type(self):
        return u'place'

    def __unicode__(self):
        return self.full_name
