
CR = "10.001025 -84.134588" # no space between

@DefaultParams =
  username: "larry"
  api_key: "d65af2857fc77e4ce56299e53f6858178dfab295"
  format: "json"
  limit: 5

class @AppData extends Backbone.Model
  defaults:
    center: CR
    zoom: 16
    mapTypeId: google.maps.MapTypeId.ROADMAP

  initialize: (attributes) ->
    ll = attributes.center.split(',')
    @set('centerLat', ll[0])
    @set('centerLng', ll[1])

# A place has a location
class @Place extends Backbone.Model
    defaults:
      notes: ''

    # Fear the XSS.
    escapedJson: ->
        return json =
            id: @get "id"

    initialize: (attributes) ->
      match = attributes.point?.match(/(\-?\d+(?:\.\d+)?)\s(\-?\d+(?:\.\d+)?)/)
      if match?
        @set('lat', match[1])
        @set('lng', match[2])

      params = {}
      params = $.param(_.defaults(params, DefaultParams))
      if @has('resource_uri')
        @url = @get('resource_uri') + "?#{params}"

      @bind 'change', @recalcPoint

    recalcPoint: =>
      if @hasChanged('lat') or @hasChanged('lng')
        lat = @get('lat')
        lng = @get('lng')
        @set('point', "POINT(#{lat} #{lng})")

    toJSON: ->
      point: @get('point')
      notes: @get('notes')

class @Places extends Backbone.Collection
  model: Place

  show: ->
    @trigger 'show'
    @each (place) => place.trigger 'show'

  hide: ->
    @trigger 'hide'
    @each (place) => place.trigger 'hide'

class @PlaceType extends Backbone.Model
  idAttribute: 'id'

  initialize: ->
    @places = new Places()

    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    @places.url = "/api/v1/place/?#{params}"
    #?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295

  show: ->
    @trigger 'show'
    @places.show()

  hide: ->
    @trigger 'hide'
    @places.hide()

class @PlaceTypes extends Backbone.Collection
  model: PlaceType
