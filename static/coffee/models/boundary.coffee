# A boundary has a location
class @Boundary extends Backbone.Model

  # Fear the XSS.
  escapedJson: ->
    return json =
      id: @get "id"

  initialize: (attributes) ->
    match = attributes.poly?.match(/(-?\d+(?:\.\d+)?)\s(-?\d+(?:\.\d+)?)/mg)
                                   
    if match?
      #console.log 'match', match
      points = (point.split(' ') for point in match)
      #console.log 'Backbone.points',  points
      latlngs = (new google.maps.LatLng(point[1], point[0]) for point in points)

      #console.log 'latlngs',  latlngs
      # for latlng in latlngs
      #   console.log 'latlng', latlng.lat(), latlng.lng()

      @set('latlngs', latlngs)

    #@set('id', attributes.id)
    @id = attributes.id
    @cid = attributes.previousnumber

    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    if @has('resource_uri')
      @url = @get('resource_uri') + "?#{params}"

  toJSON: ->
    poly: @get('poly')
