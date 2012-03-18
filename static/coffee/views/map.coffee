class @MapView extends Backbone.View
  events:
    'click button#add-place': '_addPlace'

  initialize: ->
    @preferences = @options.preferences
    @render()

  render: ->
    @map = new google.maps.Map @$('#map-canvas').get(0),
      zoom: @preferences.get('zoom')
      center: new google.maps.LatLng(@preferences.get('centerLat'), @preferences.get('centerLng'))
      mapTypeId: @model.get('mapTypeId')

      mapTypeControl: true

      mapTypeControlOptions: 
        # style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID]


    # console.log 'MapView.render zoom', @map.getZoom()

    # http://code.google.com/apis/maps/documentation/javascript/controls.html#Adding_Controls_to_the_Map
    controlDiv = document.createElement('DIV')
    controlDiv.style.padding = '5px'

    controlUI = document.createElement('DIV')
    controlUI.style.backgroundColor = 'white'
    controlUI.style.borderStyle = 'solid'
    controlUI.style.borderWidth = '2px'
    controlUI.style.cursor = 'pointer'
    controlUI.style.textAlign = 'center'
    controlUI.title = 'Click to drop a new Place Marker'
    controlDiv.appendChild(controlUI)

    controlText = document.createElement('DIV')
    controlText.style.fontFamily = 'Arial,sans-serif'
    controlText.style.fontSize = '12px'
    controlText.style.paddingLeft = '4px'
    controlText.style.paddingRight = '4px'
    controlText.innerHTML = 'Add Place'
    controlUI.appendChild(controlText)

    # google.maps.event.addListener @map, 'idle', @onIdle
    google.maps.event.addListener @map, 'maptypeid_changed', @onMapTypeChange

    google.maps.event.addDomListener controlUI, 'click', =>
      @_addPlace()

    @map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv)


    google.maps.event.addListener @map, 'zoom_changed', =>
      @preferences.set('zoom', @map.getZoom())

    @userid = @model.get('userid')
      
    if @userid > 0
      # load places
      @places = new Places()
      new PlacesView(collection: @places, map: @map)
      new ListView(collection: @places)
      @places.fetch()

      # load boundaries
      @boundaries = new Boundaries()
      new BoundariesView(collection: @boundaries, map: @map)
      @boundaries.fetch()



  _togglePlaceType: (e) ->
    inputEl = @$(e.target)
    model = @collection.get(inputEl.val())
    if inputEl.is(":checked")
      model.show()
    else
      model.hide()

  _addPlace: () ->
    lat = @map.getCenter().lat()
    lng = @map.getCenter().lng()
    @places.create(territoryno: @preferences.get('territoryno'), point: "POINT (#{lat} #{lng})")

  # When map type changes we need to change color of polygons
  # Note:  needs fat arrow because this is used as a callback

  onMapTypeChange: =>
    switch @map.getMapTypeId()
      when google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID
        @currentPolyOpts = @roadmapPolyOpts
      else
        @currentPolyOpts = @hybridPolyOpts
    