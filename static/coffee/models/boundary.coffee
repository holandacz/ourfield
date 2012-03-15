# A boundary has a location
class @Boundary extends Backbone.Model

  # Fear the XSS.
  escapedJson: ->
    return json =
      id: @get "id"

  initialize: (attributes) ->
    points = (point for point in attributes.poly?.match(/(-?\d+(?:\.\d+)?)\s(-?\d+(?:\.\d+)?)/mg))
    
    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    if @has('resource_uri')
      @url = @get('resource_uri') + "?#{params}"

  toJSON: ->
    poly: @get('poly')

