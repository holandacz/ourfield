# -*- coding: utf-8 -*-
#import wingdbstub

from django.db.models import Max
from django.db import connection, transaction
from models import Place
    
class PlaceMarkernos(currentPlace, isnew = False, isdeleted = False)
    def __init__(self, currentPlace):
        self.currentPlace = currentPlace
        self.currentPlace_id = currentPlace.id
        self.currentPlaceTerritoryno = currentPlace.territoryno
        self.currentPlaceMarkerno = currentPlace.markerno
        self.currentMaxTerritoryMarkerno = self._maxTerritoryMarkerno(currentPlace.territoryno)
        self.currentPlaceCount = self._countTerritoryPlaces(currentPlace.territoryno)

        # perform a few integrety checks
        # if currentMaxTerritoryMarkerno != currentPlaceCount
        if self.currentMaxTerritoryMarkerno != self.currentPlaceCount:
            self.fixUnnumberedMarkers()
            # recalc self.currentMaxTerritoryMarkerno
            self.currentMaxTerritoryMarkerno = self._maxTerritoryMarkerno(currentPlace.territoryno)
            print "MAX markerno did not match total number of places. Automatically numbered unnumbered markers."

        self.isnew = isnew
        self.isdeleted = isdeleted

    def _calcMarkerno(self):
        """Calculate best guess markerno based on its location"""

        # Find closest place to currentPlace 
        closestPlace = self.currentPlace.findClosestPlace()

        # Get the Place before and after the closestPlace
        nextPlace = closestPlace.adjoiningPlace()
        prevPlace = closestPlace.adjoiningPlace('before')


        # If the closestPlace is the FIRST Place with a markerno == 1,
        # need to determine whether the currentPlace should become the new markerno #1.

        if closestPlace.markerno == 1 and nextPlace:
            # if currentPlace (?) is closer than closestPlace (#1) to Place.markerno #2 (nextPlace),
            # currentPlace.markerno will become the new #2 else #1
            return 2 if self.currentPlace.calcDistanceSquare(nextPlace) < closestPlace.calcDistanceSquare(nextPlace) else 1

        # If the closestPlace is the LAST Place with a markerno == self.currentMaxTerritoryMarkerno (#MAX)
        elif closestPlace.markerno == self.currentMaxTerritoryMarkerno and prevPlace:
            # Need to determine whether the currentPlace should be the next number after(#MAX)
            # If currentPlace (?) is closer than the closestPlace (#MAX) to Place.markerno #MAX - 1 (prevPlace), 
            # currentPlace.markerno will become the new #MAX else #MAX + 1 
            if self.currentPlace.calcDistanceSquare(prevPlace) < closestPlace.calcDistanceSquare(prevPlace):
                return self.currentMaxTerritoryMarkerno
            else:
                return self.currentMaxTerritoryMarkerno + 1

        elif prevPlace and nextPlace:
            if self.currentPoint.calcDistanceSquare(prevPlace) < self.currentPoint.calcDistanceSquare(nextPlace):
                return closestPlace.markerno
            else:
                return nextPlace.markerno

        else:
            raise Exception("Expected prevPlace and nextPlace")

    def handleChange(self):
        if self.isnew:
            self._handleAdded()
        elif self.isdeleted()
            self._handleDeleted()
        else:
            self._handleChanged()  
    def fixUnnumberedMarkers(self):
        """fix rare case where marker need numbers cleaned up"""
        cursor = connection.cursor()

        # while maintaining existing order, renumber all sequentially
        newmarkerno = 1
        cursor.execute('START TRANSACTION')
        for place in Place.objects.filter(territoryno=territoryno).exclude(deleted=True).order_by('markerno'):
            sql = 'UPDATE %s SET markerno = markerno %s 1 WHERE (id = %d)' % (Place._meta.db_table, place.id, newmarkerno)
            cursor.execute(sql)
            newmarkerno += 1

        cursor.execute('COMMIT')
    def _countTerritoryPlaces(self):
        """Return total count of Places within a territory"""
        return Place.objects.filter(territoryno=self.territoryno).count()            
    def _getPreviousPlace(self):
        self.previousPlace = Place.objects.get(id = self.currentPlace_id) 
        self.previousPlace_id = self.previousPlace.id
        self.previousPlaceTerritoryno = self.previousPlace.territoryno
        self.previousPlaceMarkerno = self.previousPlace.markerno
        self.previousPlaceMaxMarkerno = self._maxTerritoryMarkerno(previousPlace.territoryno)
        self.previousPlaceCount = self._countTerritoryPlaces(previousPlace.territoryno)
        self.previousPlaceMarkernosList = self._getTerritoryMarkernos(previousPlace.territoryno)
    def _handleAdded():
        """Assign a markerno based on its location and position"""

        # NOTE: Place may be added and admin may have chosen a markerno
        if self.currentPlaceMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(greater_than = self.currentPlaceMarkerno - 1)
            return self.currentPlaceMarkerno

        # calcMarkerno
        self.currentPlaceMarkerno = self._calcMarkerno()

        # if it is not the next markerno, then it was inserted between two other markers OR is the new markerno 1
        if not self.currentPlaceMarkerno > self.currentMaxTerritoryMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(greater_than = self.currentPlaceMarkerno - 1)
            return self.currentPlaceMarkerno
    def _handleChanged():
        # get previous data in case use changed pertinent details
        self._getPreviousPlace()

        # Was this Place moved from a previous territory?
        if self.previousPlaceTerritoryno and self.currentPlaceTerritoryno != self.previousPlaceTerritoryno:
            # need to renumber Places in the territory that lost the moved Place
            # decrement prevPlace markerno's greater_than > prev_markerno, thus filling in the resulting gap
            self._updateMarkernos(self.previousPlaceTerritoryno, greater_than = prev_markerno, decrement = True) 
            
        # Place was changed but markerno was not
        if self.currentPlaceMarkerno == self.previousPlaceMarkerno:
            # calcMarkerno
            markerno = self._calcMarkerno()

            # if no change
            if markerno == self.currentPlaceMarkerno:
                return self.currentPlaceMarkerno

        # handle if target self.currentPlaceMarkerno is less than self.previousPlaceMarkerno
        if self.currentPlaceMarkerno < self.previousPlaceMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(greater_than = self.currentPlaceMarkerno - 1, less_than = self.previousPlaceMarkerno)
            return self.currentPlaceMarkerno
        
        # handle if target self.currentPlaceMarkerno is greater than self.previousPlaceMarkerno
        if self.currentPlaceMarkerno > self.previousPlaceMarkerno:
            # we have to insert and renumber other markers
            self._updateMarkernos(greater_than = self.previousPlaceMarkerno, less_than = self.currentPlaceMarkerno + 1, decrement = True)
            return self.currentPlaceMarkerno
    def _handleDeleted():
        """If Place is deleted, need to reorder other markerno's in territory"""
        # get previous data in case use changed pertinent details before clicking delete
        self._getPreviousPlace()
        
        # decrement all markernos greater than the markerno that was deleted, thus filling the gap
        self._updateMarkernos(prev_territoryno, greater_than = self.previousPlaceMarkerno, decrement = True)
    def _maxTerritoryMarkerno(self):
        """Return highest markerno within a territory"""
        result = Place.objects.filter(territoryno=self.territoryno).aggregate(Max('markerno'))
        return result['markerno__max'] if result else 0 
    def _updateMarkernos(territoryno, greater_than=0, less_than=999999999999, decrement=False, ):
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
        ''' % (Place._meta.db_table, ('-' if decrement else '+'), territoryno, greater_than, less_than)
        
        cursor.execute(sql)
        transaction.commit_unless_managed()  
