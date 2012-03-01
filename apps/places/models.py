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
from tastypie.models import create_api_key

models.signals.post_save.connect(create_api_key, sender=User)

class Place(MyModel):
    confirmed = models.BooleanField("Confirmed?",)
    territoryno = models.CharField("Territory No", max_length=6, null=True, blank=True, db_index=True, default="4-1-2")
    sortno = models.PositiveIntegerField("Sort No", null=True, default=0)
    blockno = models.CharField("Block No", max_length=32, null=True, blank=True)
    pointno = models.PositiveIntegerField("Point No", null=True, blank=True)
    markerno = models.PositiveIntegerField("Marker No", null=True, blank=True, db_index=True)
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
    geocoded = models.BooleanField("GeoCoded?", )
    multiunit = models.BooleanField("MultiUnit?", )
    residential = models.BooleanField("Residential?", default=True )
    deleted = models.BooleanField("Deleted?", db_index=True)
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
            ret += self.blockno
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
        
    @transaction.commit_manually
    def save(self, *args, **kw):
        #self.ParseDetails()
        self.geocoded = True if (self.point.y and self.point.x) else False
        
        # In order to handle renumbering of markerno's, I need to see if markno has changed.
        # If so, handle renumbering
        self._handleMarkernoChangedSave()
        
        super(Place, self).save(*args, **kw)
        
        transaction.commit()
        
    def type(self):
        return u'place'

    def __unicode__(self):
        return self.full_name


    def _updateMarkernos(self, \
            territoryno='4-1-2', \
            increment=True, \
            greater_than=0, \
            less_than=999999999999\
            ):
        
        cursor = connection.cursor()
        
        sql = '''
        update of_places 
          set markerno = markerno + 1 
        where (
          territoryno = "%s" 
          and markerno > %d
          and markerno < %d
          and markerno is not null
        )
        ''' % (territoryno, greater_than, less_than)
        
        cursor.execute(sql)
        transaction.commit_unless_managed()        










    # default markerno to be max markerno + 1
    def _handleMarkernoChangedAdded(self):
        """If Place is added, need to reorder other markerno's in territory"""
        x=0
        pass
    
    def _handleMarkernoChangedDelete(self):
        """If Place is deleted, need to reorder other markerno's in territory"""
        
        # Get previous markerno
        # update markerno's >prev_markerno to markerno + 1
        # update of_places set markerno = markerno + 1 where territoryno = '4-1-2' and markerno is not null
        x=0
        
        pass
        

    def maxMarkerno(self, territoryno):
        result = Place.objects.filter(territoryno=territoryno).aggregate(Max('markerno'))
        return result['markerno__max'] if result else 1   
                        
    def _handleMarkernoChangedSave(self):
        """If Place.markerno is changed, need to reorder other markerno's"""
        
        # this is a new Place
        if not self.id:
            # if no markerno was set
            # set it to max markerno + 1
            
            if self.territoryno and not self.markerno:
                self.markerno = self.maxMarkerno(self.territoryno) + 1
                     
            else:
                # else adjust affected markerno's
                # update of_places set markerno = markerno + 1 where territoryno = '4-1-2' and markerno is not null                   
                pass
            
        # existing Place
        else:
            # get previous data to determine how to proceed
            prevPlace = Place.objects.get(id=self.id)
            prev_id = prevPlace.id
            prev_territoryno = prevPlace.territoryno
            prev_markerno = prevPlace.markerno
        
            # if new Place.territoryno is different that previous
            # need to reorder markerno's prev_territoryno
            # need to reorder markerno's in current_territoryno
            if self.territoryno != prevPlace.territoryno:
                pass
            
            # only reorder markers in current territory
            else:
                pass
