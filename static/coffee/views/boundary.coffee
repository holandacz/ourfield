class @BoundariesView extends Backbone.View

  initialize: ->
    @map = @options.map
    @preferences = @options.preferences

    @territoryno = @preferences.get('territoryno')

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
    #console.log 'render', @territoryno
    #console.log @boundaryItemViews
    @center() if @territoryno

  center: ->
    # console.log @mapView.boundaries.get(652).attributes.latlngs
    terr = @collection.getByCid(territoryno)
    if terr?
      bounds = new google.maps.LatLngBounds()

      latlngs = terr.attributes.latlngs
      for latlng in latlngs
        bounds.extend(latlng)
        
      @map.setCenter(bounds.getCenter())

  addBoundaryItemView: (boundary) =>
    boundary.bind 'sync', =>
      @collection.fetch()
    @boundaryItemViews.push(new BoundaryItemView(collection: @collection, model: boundary, territoryno: territoryno, map: @map))

class @BoundaryItemView extends Backbone.View
  roadmapPolyOpts:
    strokeWeight: .5
    strokeColor: '#000000'
    fillColor: '#000000'
    fillOpacity: 0
    
  hybridPolyOpts:
    strokeWeight: .5
    strokeColor: '#ffffff'
    fillColor: '#ffffff'
    fillOpacity: 0
  
  hoverPolyOpts:
    strokeWeight: 2
    fillColor: '#ffd700'
    fillOpacity: 0


  initialize: ->
    @territoryno = @options.territoryno
    @collection = @options.collection
    @editing = @options.editing || false
    @map = @options.map

    @model.bind 'sync', @show
    @render()

  render: ->
    @currentPolyOpts = @roadmapPolyOpts
    @placeName = $('#placeName')
    @poly = new google.maps.Polygon(@currentPolyOpts)
    @poly.setPath(@model.get('latlngs'))
    @poly.setMap(@map)

    if window.appData.attributes['userid'] == 1
      google.maps.event.addListener @poly, "click", @edit

    google.maps.event.addListener @poly, 'mouseover', =>
      @poly.setOptions(@hoverPolyOpts)
      # @placeName.text(@model.get('id') + ' ' + @model.get('previousnumber') + ' ' + @model.get('name'))
      # @placeName.show()
      
    google.maps.event.addListener @poly, 'mousemove', =>
      @placeName.css('left', mouseX)
      @placeName.css('top', mouseY)

    google.maps.event.addListener @poly, 'mouseout', =>
      @poly.setOptions(@currentPolyOpts)
      @placeName.hide()


    @show()

    # if @territoryno == @model.attributes.previousnumber
    #   # @poly.setEditable(true)
    #   @poly.runEdit(true)

  edit: =>
    @editing = true
    console.log 'edit poly', @poly.latLngs.b[0]
    google.maps.event.addListener @poly, "rightclick", @stopedit
    @poly.runEdit(true)

  stopedit: =>
    @editing = false
    @poly.stopEdit()
    if confirm("Are you sure you want to modify this boundary?")
      #console.log 'oldPoly', @model.get('poly')

      latlngslist = (latlng.lng() + ' ' + latlng.lat() for latlng in @poly.getPath().b)
      newPoly = 'POLYGON ((' + latlngslist.toString() + '))'
      #console.log 'newPoly', newPoly
      @model.set('poly', newPoly)
      @model.save()
    # else
    #   console.log @model
    #   console.log @poly
    #   @poly.setMap(null)
    #   #@poly.setVisible(false)
    #   @collection.fetch()
    #   #@model.fetch()

    @render()

  show: =>
    # console.log 'BoundaryItemView.show'

  hide: =>
    #console.log 'BoundaryItemView.hide'
