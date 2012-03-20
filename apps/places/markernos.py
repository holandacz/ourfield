# -*- coding: utf-8 -*-
#import wingdbstub

from django.db.models import Max, Min
from django.db import connection, transaction

class PlaceMarkernos:
    def __init__(self, currentPlace = None, isnew = False, isdeleted = False):
        from models import Place
        
        if currentPlace:
            self.Place = Place
            self.currentPlace = currentPlace
            self.currentPlace_id = currentPlace.id
            self.currentPlaceTerritoryno = currentPlace.territoryno
            self.currentPlaceMarkerno = currentPlace.markerno
            self.currentMinTerritoryMarkerno = self._minTerritoryMarkerno(currentPlace.territoryno)
            self.currentMaxTerritoryMarkerno = self._maxTerritoryMarkerno(currentPlace.territoryno)
            self.currentPlaceCount = self._countTerritoryPlaces(currentPlace.territoryno)
    
            self.isnew = isnew
            self.isdeleted = isdeleted


    def automarkerno(self, start_id = None, territoryno = None):
        from models import Place
        # if a start_id given, get marker number for that id
        if start_id:
            try:
                startPlace = Place.objects.get(id=start_id)
                territoryno = startPlace.territoryno
            except:
                error = 'Invalid ID: %d' % start_id
                return 'ERROR: %s' % error
            
            start_markerno = startPlace.markerno
            
            # if are there Places that have markerno's before this markerno?
            for markerno in range(1, start_markerno):
                count = Place.objects.filter(territoryno=territoryno).filter(markerno=markerno).count()
                if not count:
                    error = 'Expected a Place with markerno = : %d' % markerno
                    return 'ERROR: %s' % error
                elif count > 1:
                    error = 'Found more than one Place with markerno = : %d' % markerno
                    return 'ERROR: %s' % error
            
            # if no more places to number
            if len(Place.objects.all()) == start_markerno:
                return True
            
            # Reset all other markerno's
            Place.objects.filter(territoryno=territoryno).filter(markerno__gt=start_markerno).update(markerno=0)        
    
            place = startPlace
            markerno = start_markerno + 1 # we already have start_markerno set
            while True:
                
                # find closest Place with markerno greater than place.markerno
                place = place.findClosestPlace(place.markerno)
                if not place:
                    break
                place.markerno = markerno
                place.save(handleMarkernos = False)
                markerno += 1
                
        else:
            # number all Places
            places = Place.objects.filter(territoryno = territoryno)
            if not places:
                return HttpResponseRedirect("/map/?territoryno=%s" % territoryno)
            
            # Reset all markerno's
            Place.objects.filter(territoryno=territoryno).update(markerno=0)
            
            # find west / left most Place within territory        
            westPlaceLng = 999999
            startPlace = None
            for place in places:        
                if place.point[1] < westPlaceLng:
                    westPlaceLng = place.point[1]
                    startPlace = place
                
                
            start_markerno = 1    
            startPlace.markerno = start_markerno
            startPlace.save(handleMarkernos = False)
            place = startPlace
            markerno = start_markerno + 1 # we already have start_markerno set
            
            # loop through all places in territory
            while True:
                
                # find closest Place with markerno greater than place.markerno
                place = place.findClosestPlace(place.markerno)
                if not place:
                    break
                place.markerno = markerno
                place.save(handleMarkernos = False)
                markerno += 1
    
        return True

    def updateMarkernos(self):
        self._updateMarkernos(self.currentPlace.territoryno, greater_than=self.currentPlace.routemarkernoafter)
        self.currentPlace.markerno = self.currentPlace.routemarkernoafter + 1
        self.currentPlace.routemarkernoafter = 0
        self.currentPlace.save(handleMarkernos = False)
        
    def _handleChanged(self):
        # get previous data in case use changed pertinent details
        self._getPreviousPlace()
        
        # Was this Place moved from a previous territory?
        # TODO: When moved to a new territoryno, NEW markerno's need adjusting!
        if self.previousPlaceTerritoryno and self.currentPlaceTerritoryno != self.previousPlaceTerritoryno:
            # need to renumber Places in the territory that lost the moved Place
            # decrement prevPlace markerno's greater_than > prev_markerno, thus filling in the resulting gap
            self._updateMarkernos(self.previousPlaceTerritoryno, greater_than = self.previousPlaceMarkerno, decrement = True) 
        
        currentMarkerno = self.currentPlace.markerno        
        
        # ignore 0 or unnumbered markers
        if not currentMarkerno:
            return currentMarkerno
                
        ## if point and markerno has not changed, return
        #if currentMarkerno == self.previousPlaceMarkerno \
           #and self.currentPlace.point.x == self.previousPlace.point.x \
           #and self.currentPlace.point.y == self.previousPlace.point.y:
            #return currentMarkerno     

        # if markerno has not changed, return
        if currentMarkerno == self.previousPlaceMarkerno:
            return currentMarkerno     

        # Place was changed but markerno was not
        if currentMarkerno != self.previousPlaceMarkerno:  
            # does the previousPlaceMarkerno exist, then just swap 
            if self.Place.objects.filter(territoryno = '4-1-2').filter(markerno=currentMarkerno).exists():
                # Let's swap self.previousPlaceMarkerno with currentMarkerno
                cursor = connection.cursor()
                
                # if there is a gap between currentMarkerno and the one previous, set markerno to become one after previous one
                # self.currentPlace.markerno
                
                # look for and update Place where markerno = new markerno and set to prev Place markerno
                sql = '''
                update %s set markerno = %d 
                where (territoryno = "%s" and markerno = %d)
                limit 1
                ''' % (self.Place._meta.db_table, self.previousPlaceMarkerno, self.currentPlaceTerritoryno, currentMarkerno)
                cursor.execute(sql)
                transaction.commit_unless_managed() 
               
            return currentMarkerno 
        
        # Place was changed/moved but markerno was not
        if currentMarkerno == self.previousPlaceMarkerno:
            # calcMarkerno
            #markerno, prevPlace, nextPlace = self._calcMarkerno()
            currentMarkerno = self._calcMarkerno()

            # if no change
            if currentMarkerno == self.currentPlace.markerno:
                return currentMarkerno

        # handle if target self.currentPlaceMarkerno is less than self.previousPlaceMarkerno
        if currentMarkerno < self.previousPlaceMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(self.currentPlaceTerritoryno, \
                                  greater_than = currentMarkerno - 1, \
                                  less_than = self.previousPlaceMarkerno)
            return currentMarkerno
        
        # handle if target currentMarkerno is greater than self.previousPlaceMarkerno
        if currentMarkerno > self.previousPlaceMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(self.currentPlaceTerritoryno, \
                                  greater_than = self.previousPlaceMarkerno - 1, \
                                  less_than = currentMarkerno + 1, \
                                  decrement = True)
            return currentMarkerno
  
    def _calcMarkerno(self):
        """Calculate best guess markerno based on its location"""

        # Find closest place to currentPlace 
        closestPlace = self.currentPlace.findClosestPlace()
        if not closestPlace:
            return 1
        
        calcedMarkerno = None
        
        # Get the Place before and after the closestPlace
        nextPlace = closestPlace.adjoiningPlace()
        # if currentPlace == nextPlace, then user is moving a Place that was already located after closestPlace
        # then get the Place AFTER nextPlace
        if nextPlace and nextPlace.id == self.currentPlace_id:
            nextPlace = nextPlace.adjoiningPlace()
        
        prevPlace = closestPlace.adjoiningPlace('before')
        # if currentPlace == prevPlace, then user is moving a Place that was already located before closestPlace
        # then get Place BEFORE prevPlace
        if prevPlace and prevPlace.id == self.currentPlace_id:
            prevPlace = prevPlace.adjoiningPlace('before')


        # If the closestPlace is the FIRST Place with a markerno == 1,
        # need to determine whether the currentPlace should become the new markerno #1.

        if closestPlace.markerno == 1 and nextPlace:
            # if currentPlace (?) is closer than closestPlace (#1) to Place.markerno #2 (nextPlace),
            # calcedMarkerno will become the new #2 else #1
            calcedMarkerno = 2 if self.currentPlace.calcDistanceSquare(nextPlace) < closestPlace.calcDistanceSquare(nextPlace) else 1
            
        elif closestPlace.markerno == 1 and not nextPlace:
            calcedMarkerno = 2
            
            
            
        # If the closestPlace is the LAST Place with a markerno == self.currentMaxTerritoryMarkerno,        
        elif closestPlace.markerno == self.currentMaxTerritoryMarkerno and prevPlace:
            # if currentPlace (?) is closer to closestPlace (#MAX) than Place.markerno #MAX-1 (prevPlace),
            # calcedMarkerno will become the new #2 else #1
            #calcedMarkerno = 2 if self.currentPlace.calcDistanceSquare(nextPlace) < closestPlace.calcDistanceSquare(nextPlace) else 1            
            if prevPlace.calcDistanceSquare(self.currentPlace) < prevPlace.calcDistanceSquare(closestPlace):
                calcedMarkerno = prevPlace.markerno
            else:
                calcedMarkerno = closestPlace.markerno
                
            if not nextPlace and self.isnew:
                calcedMarkerno += 1

        ## If the closestPlace is the LAST Place with a markerno == self.currentMaxTerritoryMarkerno (#MAX)
        #elif nextPlace and closestPlace.markerno == self.currentMaxTerritoryMarkerno and prevPlace:
            ## Need to determine whether the currentPlace should be the next number after(#MAX)
            ## If currentPlace (?) is closer than the closestPlace (#MAX) to Place.markerno #MAX - 1 (prevPlace), 
            ## currentPlace.markerno will become the new #MAX else #MAX + 1 
            #if prevPlace.calcDistanceSquare(currentPlace) < prevPlace.calcDistanceSquare(closestPlace):
                #calcedMarkerno = prevPlace.markerno
            #else:
                #calcedMarkerno = closestPlace.markerno
        
        # 
        elif not nextPlace:
            # The closestPlace does not have an nextPlace and is the current end of the list
            # Need to determine if the current place should be added to the end of the route 
            # or BEFORE the lastPast (closestPlace)
            # is currentPlace BEWTEEN closestPlace and its prevPlace?
            
            # calc distance from closestPlaceToPrevPlace
            distanceFromClosestPlaceToPrevPlace = closestPlace.calcDistanceSquare(prevPlace)
            
            # calc distance from currentPlace to closestPlace
            distanceFromCurrentPlaceToClosestPlace = self.currentPlace.calcDistanceSquare(closestPlace)
            
            # calc distance from currentPlace to prevPlace
            distanceFromCurrentPlaceToPrevPlace = self.currentPlace.calcDistanceSquare(prevPlace)
            
            # it is between closestPlace and its prevPlace
            if distanceFromCurrentPlaceToPrevPlace < distanceFromClosestPlaceToPrevPlace:
                calcedMarkerno = prevPlace.markerno + 1
            else:
                # is located AFTER last Place
                calcedMarkerno = closestPlace.markerno + 1
                    
        elif not prevPlace:
            # The closestPlace does not have an prevPlace and is the current end of the list
            # Need to determine if the current place should be added to the end of the route 
            # or BEFORE the lastPast (closestPlace)
            # is currentPlace BEWTEEN closestPlace and its nextPlace?
            
            # calc distance from closestPlaceToNextPlace
            distanceFromClosestPlaceToNextPlace = closestPlace.calcDistanceSquare(nextPlace)
            
            # calc distance from currentPlace to nextPlace
            distanceFromCurrentPlaceToNextPlace = self.currentPlace.calcDistanceSquare(nextPlace)
            
            # it is between closestPlace and its nextPlace
            if distanceFromCurrentPlaceToNextPlace < distanceFromClosestPlaceToNextPlace:
                calcedMarkerno = closestPlace.markerno
            else:
                # is located BEFORE first Place
                calcedMarkerno = closestPlace.markerno - 1    
                
        elif prevPlace and nextPlace:
            
            mostInLineWithPlace = self.currentPlace.mostInLineWith(closestPlace, prevPlace, nextPlace)
            
            if mostInLineWithPlace.markerno == prevPlace.markerno:
                calcedMarkerno = prevPlace.markerno
            else:
                calcedMarkerno = closestPlace.markerno
                
            if self.isnew:
                calcedMarkerno += 1
                
            # forgot why this
            if hasattr(self, 'previousPlaceMarkerno') and self.previousPlaceMarkerno > calcedMarkerno:
                calcedMarkerno += 1

        else:
            raise Exception("Expected prevPlace and nextPlace")
        
            
        return calcedMarkerno

    def handleChange(self):
        if self.isnew:
            #print 'Added'
            self.currentPlace.markerno = self._handleAdded()
        elif self.isdeleted:
            #print 'Deleted'
            self._handleDeleted()
        else:
            #print 'Changed'
            self.currentPlace.markerno = self._handleChanged()  
    def _countTerritoryPlaces(self, territoryno):
        """Return total count of Places within a territory"""
        return self.Place.objects.filter(territoryno=territoryno).count()            
    def _getPreviousPlace(self):
        
        # Get the previous place realizing that there MAY be a gap
        self.previousPlace = self.currentPlace.adjoiningPlace(adjoin = 'before')
        
        self.previousPlace = self.Place.objects.get(id = self.currentPlace_id) 
        self.previousPlace_id = self.previousPlace.id
        self.previousPlaceTerritoryno = self.previousPlace.territoryno
        self.previousPlaceMarkerno = self.previousPlace.markerno
        self.previousPlaceMaxMarkerno = self._maxTerritoryMarkerno(self.previousPlace.territoryno)
        self.previousPlaceCount = self._countTerritoryPlaces(self.previousPlace.territoryno)
        
    def reorderAllMarkernos(self):
        pass
    
    def _handleAdded(self):
        """Assign a markerno based on its location and position"""

        # NOTE: Place may be added and admin may have chosen a markerno
        if self.currentPlaceMarkerno:
            
            #if self.currentPlaceMarkerno == 1:
                #self._reorderAllMarkernos()
            #else:
                ## we have to insert and renumber other markers
                #self._updateMarkernos(self.currentPlaceTerritoryno, greater_than = self.currentPlaceMarkerno - 1)
            
            self._updateMarkernos(self.currentPlaceTerritoryno, greater_than = self.currentPlaceMarkerno - 1)
            
            return self.currentPlaceMarkerno

        # calcMarkerno
        currentMarkerno = self._calcMarkerno()

        # if it is not the next markerno, then it was inserted between two other markers OR is the new markerno 1
        if not currentMarkerno > self.currentMaxTerritoryMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(self.currentPlaceTerritoryno, greater_than = currentMarkerno - 1)
        return currentMarkerno
          
            
    def _handleDeleted(self):
        """If Place is deleted, need to reorder other markerno's in territory"""
        # get previous data in case use changed pertinent details before clicking delete
        self._getPreviousPlace()
        
        # decrement all markernos greater than the markerno that was deleted, thus filling the gap
        self._updateMarkernos(self.previousPlaceTerritoryno, greater_than = self.previousPlaceMarkerno, decrement = True)
    def _maxTerritoryMarkerno(self, territoryno):
        """Return highest markerno within a territory"""
        result = self.Place.objects.filter(territoryno=territoryno).aggregate(Max('markerno'))
        return result['markerno__max'] if result else 0 
    def _minTerritoryMarkerno(self, territoryno):
        """Return lowest markerno within a territory"""
        result = self.Place.objects.filter(territoryno=territoryno).aggregate(Min('markerno'))
        return result['markerno__min'] if result else 0     
    def _updateMarkernos(self, territoryno, greater_than=0, less_than=999999999999, decrement=False ):
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
        ''' % (self.Place._meta.db_table, ('-' if decrement else '+'), territoryno, greater_than, less_than)
        
        cursor.execute(sql)
        transaction.commit_unless_managed()  
