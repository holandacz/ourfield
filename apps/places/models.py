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
    geocoded = models.BooleanField("GeoCoded?", )
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
        
    @transaction.commit_manually
    def delete(self, *args, **kw):
        # If so, handle renumbering
        self._handleMarkernoDeleted()
        
        super(Place, self).delete(*args, **kw)
        
        transaction.commit()     
        
    def _handleMarkernoDeleted(self):
        """If Place is deleted, need to reorder other markerno's in territory"""
        # get previous data in case use changed pertinent details before clicking delete
        prevPlace = self.prevPlace()
        prev_territoryno = prevPlace.territoryno
        prev_markerno = prevPlace.markerno
        
        self.territoryno = prev_territoryno
        self.markerno = prev_markerno
        
        self._updateMarkernos(greater_than = prev_markerno, decrement = True)
        
    def type(self):
        return u'place'

    def __unicode__(self):
        return self.full_name


    
    def _getTerritoryMarkernos(self):
        return Place.objects.filter(territoryno=self.territoryno).filter(markerno__gt=0).values_list('markerno', flat=True).order_by('markerno')
    
    def _updateMarkernos(self, \
            greater_than=0, \
            less_than=999999999999, \
            decrement=False, \
            ):
        
        cursor = connection.cursor()
        
        sql = '''
        update %s 
          set markerno = markerno %s 1 
        where (
          territoryno = "%s" 
          and markerno > %d
          and markerno < %d
          and markerno is not null
        )
        ''' % (self._meta.db_table, ('-' if decrement else '+'), self.territoryno, greater_than, less_than)
        
        cursor.execute(sql)
        transaction.commit_unless_managed()  

    def _getNextTerritoryPlaceMarkerno(self):
        """Determine the next markerno to use"""
        
        # if self.max_markerno == 0
        if self.max_markerno == 0:
            return 1
            
        # All markerno's SHOULD be number 1 through total number markers
        # if not, there are some markers that have not yet been assigned markerno
        # assume self.max_markerno is NOT greater than self.countTerritoryPlaces
        
        # if there are not markerno's in this territory
        if not self.existing_markernos:
            return 1
        

        # if the first markerno is NOT 1
        if self.existing_markernos[0] != 1:
            # return one less than first one
            return self.existing_markernos[0] - 1
        
        
        next_markerno = 0
        # loop through looking for an opening gap
        for i, markerno in enumerate(self.existing_markernos):
            if i == 0:
                continue
            
            # if markerno is not 1 + previous
            if markerno != self.existing_markernos[i - 1] + 1:
                # return previous markerno + 1
                return self.existing_markernos[i - 1] + 1
        
        # if we arrive here, there was only one markerno or the next open slot is at the end of list
        
        return self.max_markerno + 1
            
    
    def _handleMarkernoChanged(self):
              
        prev_territoryno = None
        prev_markerno = None     
        
        # is this an existing place?
        if self.id:
            # get previous data to determine how to proceed
            prevPlace = self.prevPlace()
            prev_territoryno = prevPlace.territoryno
            prev_markerno = prevPlace.markerno
            
            #if no change return
            if self.territoryno == prev_territoryno and self.markerno == prev_markerno:
                return
            
            
            # Was this Place moved from a previous territory?
            # if territoryno != to prevPlace.territoryno
            # need to renumber Places in the territory that lost the moved Place
            if prev_territoryno and self.territoryno != prev_territoryno:
                # decrement prevPlace markerno's greater_than > prev_markerno
                self._updateMarkernos(prev_territoryno, \
                                      greater_than = prev_markerno, \
                                      decrement = True)
                # If moved, unset markerno if same as prev_markerno to force placing it at the end of the list
                if self.markerno == prev_markerno:
                    self.markerno = None
                
                
        
            # if the markerno is NOT set
            # AND it WAS set before, pull it out and assign it the next valid markerno
            if not self.markerno and prev_markerno:
                # decrement prevPlace markerno's greater_than > prev_markerno
                # this will close the gap in markerno's
                self._updateMarkernos(self.territoryno, \
                                      greater_than = prev_markerno, \
                                      decrement = True)
                self.markerno = _getNextTerritoryPlaceMarkerno()
                return
                                          
            
        # handle if markerno is total count of Territory Places or less than 1
        # TODO: should be put in validate
        if not self.markerno or self.markerno > self.countTerritoryPlaces or self.markerno < 1:
            self.markerno = self.next_markerno
            return
        
        
        # if markerno does NOT exist
        # go ahead and use this markerno cause user must be targeting a valid position
        if self.markerno and not self.markerno in self.existing_markernos:
            return
            
            
        # handle if target markerno is less than prev_markerno
        if self.markerno < prev_markerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(decrement = False, greater_than = self.markerno - 1, less_than = prev_markerno)
            return
            
        
        # handle if target markerno is greater than prev_markerno
        if self.markerno > prev_markerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(decrement = True, greater_than = prev_markerno, less_than = self.markerno + 1)
            return
                    
            
        
        # if user enters a markerno that is an existing markerno
        # we have to insert and renumber other markers
        self._updateMarkernos(decrement = False, greater_than = self.markerno - 1)


    def maxTerritoryMarkerno(self):
        """Return highest markerno within a territory"""
        result = Place.objects.filter(territoryno=self.territoryno).aggregate(Max('markerno'))
        return result['markerno__max'] if result else 0
    
    def countTerritoryPlaces(self):
        """Return total count of Places within a territory"""
        return Place.objects.filter(territoryno=self.territoryno).count()            

    def prevPlace(self):
        """Return previous Place for reviewing pre_update values"""
        return Place.objects.get(id=self.id)          

    def _handleMarkernoChangedSave(self):
        """If Place.markerno is changed, need to reorder other markerno's"""
        
        # we are going to only focus on Places with territoryno        
        if not self.id and not self.territoryno:
            self.markno = 0
            return
        
        # get existing markerno's for this territory, in ascend order
        self.existing_markernos = self._getTerritoryMarkernos()         
        self.max_markerno = self.maxTerritoryMarkerno()
        self.countTerritoryPlaces = self.countTerritoryPlaces()   
        self.next_markerno = self._getNextTerritoryPlaceMarkerno()

        # this is a NEW Place        
        if not self.id:
            # if markerno NOT was set
            if not self.markerno:
                self.markerno = self.next_markerno
                
                
        self._handleMarkernoChanged()