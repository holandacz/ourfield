class @Boundaries extends Backbone.Collection
  model: Boundary

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
    @url = "/api/v1/boundary/?#{params}"

  show: ->
    @trigger 'show'
    @each (boundary) => boundary.trigger 'show'

  hide: ->
    @trigger 'hide'
    @each (boundary) => boundary.trigger 'hide'

class @BoundaryType extends Backbone.Model
  idAttribute: 'id'

  initialize: ->
    @boundaries = new Boundaries()

    # params = {}
    # params = $.param(_.defaults(params, DefaultParams))
    # @boundaries.url = "/api/v1/boundary/?#{params}"
    #?username=larry;api_key=d65af2857fc77e4ce56299e53f6858178dfab295

  show: ->
    @trigger 'show'
    @boundaries.show()

  hide: ->
    @trigger 'hide'
    @boundaries.hide()

class @BoundaryTypes extends Backbone.Collection
  model: BoundaryType
