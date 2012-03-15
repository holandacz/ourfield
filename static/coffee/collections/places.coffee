class @Places extends Backbone.Collection
  model: Place

  initialize: (models, options) ->
    @queryParams = {}
    @resetUrl()

  setQueryParam: (name, value) ->
    @queryParams[name] = value
    @resetUrl()

  resetUrl: ->
    params = $.param(_.defaults(@queryParams, DefaultParams))
    #
    # Would like to determine bounds of points in this collection and then set center and best fit zoom
    #
    @url = "/api/v1/place/?#{params}"

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

    # params = {}
    # params = $.param(_.defaults(params, DefaultParams))
    # @places.url = "/api/v1/place/?#{params}"
    #?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295

  show: ->
    @trigger 'show'
    @places.show()

  hide: ->
    @trigger 'hide'
    @places.hide()

class @PlaceTypes extends Backbone.Collection
  model: PlaceType
