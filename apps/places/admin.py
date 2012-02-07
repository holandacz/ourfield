from django.contrib import admin
#from django.contrib.gis import admin
from places.models import Place

#class PlaceAdmin(admin.OSMGeoAdmin):
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('provinceno', 'cantonno', 'districtno', 'districtname', 'territoryno', 'sortno', 'blockno', 'pointno', 'isgeocoded', 'isconfirmed')
    list_filter = ('provinceno', 'cantonno', 'districtno', 'districtname', 'territoryno')
    ordering = ('provinceno', 'cantonno', 'districtno', 'territoryno', 'sortno')    
    #options = {
        #'layers': ['google.streets', 'google.hybrid'],
    #}
    #list_map = ['point']
    
    
admin.site.register(Place, PlaceAdmin)
