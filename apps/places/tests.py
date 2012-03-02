from django.test import TestCase
from django.core.management import call_command
from models import Place
import wingdbstub



class PlacesTestCase(TestCase):
    
    #from django.core.serializers import serialize
    #from app.models import Currency
    #print serializers.serialize("yaml", Currency.objects.all())
    
    # python manage.py dumpdata places --indent=4 > private/fixtures/places_testdata.json
    # python manage.py dumpdata places --indent=4 > private/fixtures/places_testdata.yaml
    
    
    # python manage.py dumpdata places > app/places/fixtures/places_testdata.json
    
    # management command to generate yaml for places
    # db places-genYamlTestData 0
    
    # load data back into db ... careful!
    # m loaddata fixtures/places_testdata.yaml
    
    fixtures = ['places_testdata']    
    def setUp(self):
	self.territoryno = '4-1-2'
	
    def test_maxTerritoryMarkerno(self):
    	p = Place()
    	self.assertEqual(p.maxTerritoryMarkerno(self.territoryno), 4)
	
    def test_saveNewTerritoryMarkerno(self):
    	p = Place()
	p.territoryno = '4-1-2'
	p.markerno = 0
	p.point = 'POINT (10.0020913639611000 -84.1346389023033940)'	
	p.save()
	x=0


