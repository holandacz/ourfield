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



def _getTerritoryMarkernos(self, territoryno='4-1-2'):
    return Place.objects.filter(territoryno=territoryno).filter(markerno__isnull=False).values('id', 'markerno').order_by('markerno')

def _updateMarkernos(self, \
        territoryno='4-1-2', \
        greater_than=0, \
        less_than=999999999999, \
        decrement=False, \
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

def _getNextTerritoryPlaceMarkerno(self):
    """Determine the next markerno to use"""
    
    # if self.max_markerno == 0
    if self.max_markerno == 0:
        return 1
        
    # All markerno's SHOULD be number 1 through total number markers
    # if not, there are some markers that have not yet been assigned markerno
    # go ahead and set markerno = self.countTerritoryPlaces + 1
    # assume self.max_markerno is NOT greater than self.countTerritoryPlaces
    
    # is there a gap in the numbering?
    elif self.max_markerno > self.countTerritoryPlaces:
        # find first open slot in array of markerno's
        
        markernos = self._getTerritoryMarkernos(self.territoryno)
        
        # if there are not markerno's in this territory
        if not markernos:
            return 1
        
        markernoslist = [m['markerno'] for m in markernos]

        # if the first markerno is NOT 1
        if markernoslist[0] != 1:
            # return one less than first one
            return markernoslist[0] - 1
        
        
        next_markerno = 0
        # loop through looking for an opening gap
        for i, markerno in enumerate(markernoslist):
            if i == 0:
                continue
            
            # if markerno is not 1 + previous
            if markerno + 1 != markernoslist[i - 1]:
                # return previous markerno + 1
                return markernoslist[i - 1] + 1
        
        # if we arrive here, there was only one markerno or the next open slot is at the end of list
    
    return self.max_markerno + 1
        

def _handleMarkernoChanged(self):
    # get previous data to determine how to proceed
    prevPlace = self.prevPlace()
    prev_territoryno = prevPlace.territoryno
    prev_markerno = prevPlace.markerno
    
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
                                  
        
    next_markerno = _getNextTerritoryPlaceMarkerno()
    
    # handle if markerno is total count of Territory Places or less than 1
    # TODO: should be put in validate
    if not self.markerno or self.markerno > self.countTerritoryPlaces or self.markerno < 1:
        self.markerno = next_markerno
        return
    
    # if user enters a markerno that is NOT the next logical markerno
    if self.markerno != next_markerno:
        # then we have to insert and renumber other markers
        self._updateMarkernos(self.territoryno, decrement = False, greater_than = self.markerno - 1)

def _handleMarkernoChangedDelete(self):
    """If Place is deleted, need to reorder other markerno's in territory"""
    
    # Get previous markerno
    # update markerno's >prev_markerno to markerno + 1
    # update of_places set markerno = markerno + 1 where territoryno = '4-1-2' and markerno is not null
    x=0
    pass

def maxTerritoryMarkerno(self, territoryno):
    """Return highest markerno within a territory"""
    result = Place.objects.filter(territoryno=territoryno).aggregate(Max('markerno'))
    return result['markerno__max'] if result else 1   

def countTerritoryPlaces(self, territoryno):
    """Return total count of Places within a territory"""
    return Place.objects.filter(territoryno=territoryno).count()            

def prevPlace(self):
    """Return previous Place for reviewing pre_update values"""
    return Place.objects.get(id=self.id)          

def _handleMarkernoChangedSave(self):
    """If Place.markerno is changed, need to reorder other markerno's"""
    
    # this is a NEW Place        
    if not self.id:
        # we are going to only focus on Places with territoryno
        if not self.territoryno:
            return
    
        self.max_markerno = self.maxTerritoryMarkerno(self.territoryno)
        self.countTerritoryPlaces = self.countTerritoryPlaces(self.territoryno)
        
        # if markerno NOT was set
        if not self.markerno:
            self.markerno = _getNextTerritoryPlaceMarkerno()
        
    self._handleMarkernoChanged()