class @BoundariesView extends Backbone.View

  initialize: ->
    @map = @options.map
    @boundaryItemViews = []
    # @boundaries.bind 'add', @addBoundaryItemView
    @collection.bind 'sync', =>
      @collection.fetch()
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
  roadmapPolyOpts:
    strokeWeight: .5
    strokeColor: '#000000'
    fillColor: '#000000'
    fillOpacity: 0.3
    
  hybridPolyOpts:
    strokeWeight: .5
    strokeColor: '#ffffff'
    fillColor: '#ffffff'
    fillOpacity: 0.3
  
  hoverPolyOpts:
    strokeWeight: 2
    fillColor: '#ffd700'
    fillOpacity: 0.01


  initialize: ->
    @map = @options.map

    @model.bind 'sync', @show
    @render()

  render: ->
    @currentPolyOpts = @roadmapPolyOpts
    @placeName = $('#placeName')
    poly = new google.maps.Polygon(@currentPolyOpts)
    poly.setPath(@model.get('latlngs'))
    poly.setMap(@map)

    google.maps.event.addListener poly, 'mouseover', =>
      poly.setOptions(@hoverPolyOpts)
      @placeName.text(@model.get('previousnumber') + ' ' + @model.get('name'))
      @placeName.show()
      
    google.maps.event.addListener poly, 'mousemove', =>
      @placeName.css('left', mouseX)
      @placeName.css('top', mouseY)

    google.maps.event.addListener poly, 'mouseout', =>
      poly.setOptions(@currentPolyOpts)
      @placeName.hide()


    @show()

  show: =>
    # console.log 'BoundaryItemView.show'

  hide: =>
    #console.log 'BoundaryItemView.hide'
