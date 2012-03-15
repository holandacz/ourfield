class @BoundariesView extends Backbone.View
  initialize: ->
    @map = @options.map
    @boundaryItemViews = []
    @boundaries.bind 'add', @addBoundaryItemView
    # @collection.bind 'sync', =>
    #   @collection.fetch()
    @boundaries.bind 'reset', @render
    @render() if @boundaries.length > 0

  render: =>
    _.each @boundaryItemViews, (boundaryItemView) =>
      boundaryItemView.hide()
    @boundaryItemViews = []
    @boundaries.each @addBoundaryItemView

  addBoundaryItemView: (boundary) =>
    boundary.bind 'sync', =>
      @boundaries.fetch()
    @boundaryItemViews.push(new BoundaryItemView(model: boundary, map: @map))

class @BoundaryItemView extends Backbone.View
  initialize: ->
    @map = @options.map

    @model.bind 'sync', @show
    @render()

  render: ->
    @position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))


