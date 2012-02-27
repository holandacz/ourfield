from django.contrib import admin
#from django.contrib.gis import admin
from places.models import Place

#class PlaceAdmin(admin.OSMGeoAdmin):
class PlaceAdmin(admin.ModelAdmin):
    #list_display = ('id', 'territoryno', 'sortno', 'provinceno', 'cantonno', 'districtno', 'districtname', 'blockno', 'pointno', 'directions', 'geocoded', 'confirmed', 'deleted')
    list_display = ('id', 'territoryno', 'sortno', 'blockno', 'houseno', 'persons', 'interestlevel', 'geocoded', 'confirmed', 'deleted')
    #list_filter = ('territoryno', 'sourcetype', 'provinceno', 'cantonno', 'districtno', 'districtname', 'geocoded', 'confirmed', 'deleted')
    list_filter = ('territoryno', 'sourcetype', 'interestlevel', 'geocoded', 'confirmed', 'deleted')
    #ordering = ('provinceno', 'cantonno', 'districtno', 'territoryno', 'sortno')    
    ordering = ('territoryno', 'sortno')    
    #options = {
        #'layers': ['google.streets', 'google.hybrid'],
    #}
    #list_map = ['point']
    
    
admin.site.register(Place, PlaceAdmin)
