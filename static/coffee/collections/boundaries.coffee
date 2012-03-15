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

