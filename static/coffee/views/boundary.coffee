class @BoundariesView extends Backbone.View
  initialize: ->
    @map = @options.map
    @boundaryItemViews = []
    @collection.bind 'add', @addBoundaryItemView
    # @collection.bind 'sync', =>
    #   @collection.fetch()
    @collection.bind 'reset', @render
    @render() if @collection.length > 0

  render: =>
    _.each @boundaryItemViews, (boundaryItemView) =>
      boundaryItemView.hide()
    @boundaryItemViews = []
    @collection.each @addBoundaryItemView

  addBoundaryItemView: (boundary) =>
    boundary.bind 'sync', =>
      @collection.fetch()
    @boundaryItemViews.push(new BoundaryItemView(model: boundary, map: @map))

class @BoundaryItemView extends Backbone.View
  initialize: ->
    @map = @options.map
    @model.bind 'show', @show
    @model.bind 'hide', @hide

    @model.bind 'sync', @show
    @render()

  render: ->
    @show()

  show: =>
    @position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))
    @marker.setPosition(@position)
    
    @marker.setMap(@map)

  hide: =>
    @marker.setMap(null)
