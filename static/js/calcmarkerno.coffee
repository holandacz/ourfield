# Plac
# markerno (Each Place has a markerno numbered between 1 and the total number of Places)
# Places = (collection of Places belonging to a territory)
# In a collection of Places, calc the markerno (markerno) given the location of a newly added or dragged Place.
# Place is included in collection
# CP = Closest Place from Place


After Place.dragend or Place.dropNew
  Place.markerno = @Places.calcMarkerno(Place)


class Point
  constructor: (@x, @y) ->
  distance_from: (p2) ->
    dx = p2.x - @x
    dy = p2.y - @y
    Math.sqrt dx*dx + dy*dy

# A place has a location
class @Place extends Backbone.Model
  initialize: (attributes) ->
    id
    lat
    lng
    markerno



class @Places extends Backbone.Collection

  # loop through all Places and look for the closest other Place in the collection
  findClosestPlace: (Place) ->
    numPlaces = len(Places)

    placePoint = new Point(Place.lat, Place.lng)
    placeId = Place.id
    minDistance = 999999999
    closestPlace = null
    for each otherPlace in Places:
      # ignore if same as base Place 
      if otherPlace.id == placeId:
        continue

      otherPlacePoint = new Point(otherPlace.lat, otherPlace.lng)
      distance = placePoint.distance_from(otherPlacePoint)
      if distance < minDistance
        closestPlace = otherPlace
        minDistance = distance



    return min( ((@distSquared(Place, Places[i]), i)
      for i in range(numPlaces-1)))[1]

  calcMarkerno: (Place) ->

    if len(self) == 1
      # Only ONE Place in Places collection
      # markerno should be 1
      return 1

    if len(self) == 2 
      # Only TWO Places in Places collection 
      # Place markerno = 0, must a new Place, return 2 for the second Place
      # Otherwise, return existing markerno because user only moving the marker
      return 2 if Place.markerno == 0 else Place.markerno
  
    # loop through Places in collection and find the closest Place. Obviously, ignore passed in Place


ptsdict = []

ptsdict.append({'id': 2950, 'markerno': 1, 'lat': 9.9973401537066309, 'lng': -84.1365272371178037})
ptsdict.append({'id': 2844, 'markerno': 2, 'lat': 9.9973537362948903, 'lng': -84.1340438220901063})
ptsdict.append({'id': 2843, 'markerno': 3, 'lat': 9.9982380000000006, 'lng': -84.1341319999999939})
ptsdict.append({'id': 2846, 'markerno': 4, 'lat': 9.9989120000000007, 'lng': -84.1355080000000015})
ptsdict.append({'id': 2845, 'markerno': 5, 'lat': 9.9991730000000008, 'lng': -84.1357280000000003})

basepointdict = {'id': 2952, 'markerno': 6, 'lat': 9.9979186377172002, 'lng': -84.1340730158692054}

class @Places extends Backbone.Collection
places = new Places()
places.reset(ptsdict)

Place.markerno = 5


class @PlaceItemView extends Backbone.View
  initialize: ->
    @render()

  render: ->
    google.maps.event.addListener @marker, "dragend", @dragend
    google.maps.event.addListener @marker, "click", @click

    @show()

# A place has a location
class @Place extends Backbone.Model
  initialize: (attributes) ->

  # this will be called after dragend or drop a new Place
  dragend: ->
    @set('NKO', @calcMKN(self))

class @Places extends Backbone.Collection
  model: Place


@calcMKN: (Place, Places) ->

  findClosestPlace: (Place, Places) ->
    numPoints = len(Places)
    return min( ((@distSquared(Place, Places[i]), i)
      for i in range(numPoints-1)))[1]  

  # find the closest Place to Place
  closestPlace = @findClosestPlace(Place, Places)

  # is closestPlace markerno == 1
  if closestPlace.markerno == 1
    # which is closer to markerno 2, closestPlace (#1) or Place?
    # If Place is closer to markerno 2, then make Place.markerno = 2. That will essentially insert Place as the new #2
    # If closestPlace (#1) is closer to Place (#2), then make Place as the new #1. That will essentially insert Place as the new #1
    return 1



# Lightweight JS objects (with CS sugar).
point =
  x: 5
  y: 3
 
console.log point.x, point.y # 5 3
 
p1 = new Point(1, 6)
p2 = new Point(6, 18)
console.log p1 # { x: 1, y: 6 }
console.log p1.distance_from # [Function]
console.log p1.distance_from p2 # 13



