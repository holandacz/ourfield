from django.contrib.gis import admin
#from olwidget.admin import GeoModelAdmin
from boundaries.models import Boundary, BoundaryType, BoundariesRelated

# Customize the map
class BoundaryAdmin(admin.OSMGeoAdmin):
    options = {
        'layers': ['google.streets', 'google.hybrid'],
    }
    list_map = ['poly']
    list_display = ('id', 'previousnumber', 'name', 'boundary_type')
    
    list_filter = ('boundary_type',)
    ordering = ('previousnumber', )   
    
class BoundaryTypeAdmin(admin.ModelAdmin):
    pass

class BoundariesRelatedAdmin(admin.ModelAdmin):
    pass

admin.site.register(Boundary, BoundaryAdmin)
admin.site.register(BoundaryType, BoundaryTypeAdmin)
admin.site.register(BoundariesRelated, BoundariesRelatedAdmin)

