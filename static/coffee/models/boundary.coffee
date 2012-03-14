# A boundary has a location
class @Boundary extends Backbone.Model

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

  toJSON: ->
    point: @get('point')
    territoryno: @get('territoryno') 

