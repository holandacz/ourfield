# https://github.com/zacharyvoase/django-boss
# http://docs.python.org/dev/library/argparse.html
from djboss.commands import *
# a copy of this file should be copied to djboss app dir
import wingdbstub

@command
@argument('howmany', type=int, help="How many notes to list. 0 for all.")   
def places_html2text(args):
    """Convert html to text and put into notes field."""
    import html2text
    #from BeautifulSoup import BeautifulSoup
    

    howmany = 0 if args.howmany <= 0 else args.howmany
    from places.models import Place

    # only records that have data in noteshtml
    placeslist = Place.objects.filter(noteshtml__isnull=False)
    #placeslist = Place.objects.all()
    if howmany > 0:
	placeslist = placeslist[:howmany]
	
    for place in placeslist:
	print place.id
	
	mkhtml = html2text.HTML2Text()
	mkhtml.ignore_links = False    	
	text = mkhtml.handle(place.noteshtml)
	text = text.strip()
	text = text.replace('\n\n', '\n')
	place.notes = text
	place.save()
    
	x = 0


@command
@argument('howmany', type=int, help="How many notes to list. 0 for all.")   
def places_strip_enml(args):
    """Strip ENML from noteshtml."""
    import re
    
    howmany = 0 if args.howmany <= 0 else args.howmany
    from places.models import Place

    # only records that have data in noteshtml
    placeslist = Place.objects.filter(noteshtml__isnull=False)
    #placeslist = Place.objects.all()
    if howmany > 0:
	placeslist = placeslist[:howmany]
	
    for place in placeslist:
	if 'DOCTYPE en-note' in place.noteshtml:
	    #reobj = re.compile(r"^.*?<en-note.*?>\s*(?P<html>.*?)\s*<\?xml.*?>", re.DOTALL)
	    reobj = re.compile(r"^.*?<en-note.*?>[\rn]*(?P<html>.*?)[\\rn]*</en-note>", re.DOTALL)
	    match = reobj.search(place.noteshtml)
	    # cases where enml is empty
	    if match:
	    
		html = match.group("html").strip() 
		place.noteshtml = html
		place.save()
		print place.id;
	    
		x = 0
    

    


# Load all XLS house data
@command
@argument('howmany', type=int, help="How many to load. 0 for all.")    
def loadxlsdata(args):
    import settings
    import re
    
    from places.models import Place
    
    filepath = settings.XLSDIR + '\\xls.dat' 
    lines = [line.strip() for line in open(filepath)]
    
    howmany = 0 if args.howmany <= 0 else args.howmany 
    
    reobj = re.compile(r"\d+-\d+-(?P<districtno>\d+)")    
    linecount = 0
    for line in lines:
        if line and line[0].isalpha():
            # get district number from this string
	    match = reobj.search(line)
	    if not match:
		raise Exception("Failed to find expected district number")
	    districtno = int(match.group("districtno"))
            continue
	elif line and line[0] == '{':
	    pass
	else:
	    continue
        
        rec = eval(line)
        p = Place()
        p.provinceno = rec['provinceno']
        p.districtno = districtno
        p.cantonno = rec['districtno']
        p.territoryno = rec['territoryno']
        p.blockno = rec['blockno'] if 'blockno' in rec else None
        p.houseno = rec['houseno']
        p.districtname = rec['districtname']
        p.directions = rec['directions']
        p.notes = rec['notes']
        p.save()
        
        linecount += 1
        if linecount and linecount == howmany:
            break
    
    #for note in cn.getAllNotes(notebookName, howmany):
        #try:
            #en = ENNote.objects.get(guid=note.guid)
            #print "Exists:", en.guid, en.title
            #continue
        #except:
            #en = ENNote()
            
        #withContent = True
        #withResourcesData = False
        #withResourcesRecognition = False
        #withResourcesAlternateData = False
        #notefull = cn.noteStore.getNote(cn.authToken, note.guid, withContent, withResourcesData, withResourcesRecognition, withResourcesAlternateData)        
        
        #en.UpdateFromEN(notefull, notebookName)
        #print "Added:", en.guid, en.title
        
        #notecount += 1
        #if howmany and notecount == howmany:
            #break
        
    