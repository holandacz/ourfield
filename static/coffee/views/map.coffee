class @MapView extends Backbone.View

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

  events:
    'click input[type="checkbox"]': '_togglePlaceType'
    'click button#add-place': '_addPlace'

  initialize: ->
    @preferences = @options.preferences
    @polys = {}
    @render()

  render: ->
    #console.log 'preferences', @preferences.items

    @placeName = $('#placeName')
    @currentPolyOpts = @roadmapPolyOpts
    @map = new google.maps.Map @$('#map-canvas').get(0),
      zoom: @preferences.get('zoom')
      # center: new google.maps.LatLng(@model.get('centerLat'), @model.get('centerLng'))
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

    google.maps.event.addListener @map, 'idle', @onIdle
    google.maps.event.addListener @map, 'maptypeid_changed', @onMapTypeChange

    google.maps.event.addDomListener controlUI, 'click', =>
      @_addPlace()

    @map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv)


    google.maps.event.addListener @map, 'zoom_changed', =>
      @preferences.set('zoom', @map.getZoom())

    @userid = @model.get('userid')

    # google.maps.event.addListener @map, "click", => @addPlace()
    # location: event.latLng
    # centered: false

    # if @userid > 0
    #   @boundaries = new BoundariesView(model: boundary, collection: boundaries, map: @map)
    #   console.log '@boundaries = new BoundariesView'

      
    if @userid > 0
      @collection.each (placeType) =>
        new PlaceTypeView(model: placeType, collection: placeType.places, map: @map)

      @$('input[type="checkbox"]:checked').each (index, el) =>
        model = @collection.get($(el).val())
        model.show()



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
    console.log 'preferences', @preferences.items
    @collection.get(1).places.create(territoryno: @preferences.get('territoryno'), point: "POINT (#{lat} #{lng})")

  onIdle: =>
    showError(off)
    showBusy(on)
    bounds = @map.getBounds()
    sw = bounds.getSouthWest()
    ne = bounds.getNorthEast()


    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    # if @has('resource_uri')
    #   @url = @get('resource_uri') + "?#{params}"
    # console.log params

    # $.get '/api/places', { swLat: sw.lat(), swLng: sw.lng(), neLat: ne.lat(), neLng: ne.lng() }, (data) =>
    $.get '/api/v1/boundary/?' + params, (data) =>
      poly.setMap(null) for id, poly of @polys
      @polys = {}
      #console.log 'call createPoly'

      @createPoly(poly) for poly in data.objects
      @test = 7
      showBusy(off)
    
    console.log '@currentPoly', @currentPoly
    console.log '@test', @test
    showBusy(off)

  # When map type changes we need to change color of polygons
  # Note:  needs fat arrow because this is used as a callback

  onMapTypeChange: =>
    switch @map.getMapTypeId()
      when google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID
        @currentPolyOpts = @roadmapPolyOpts
      else
        @currentPolyOpts = @hybridPolyOpts
    
  # Add a polygon to our map
  #
  createPoly: (placepoly) ->
    poly = new google.maps.Polygon(@currentPolyOpts)

    points = (point.split(' ') for point in placepoly.poly?.match(/(-?\d+(?:\.\d+)?)\s(-?\d+(?:\.\d+)?)/mg))
    lls = (new google.maps.LatLng(point[1], point[0]) for point in points)

    poly.setPath(lls)
    poly.setMap(@map)

    @polys[placepoly.id] = placepoly

    google.maps.event.addListener poly, 'mouseover', =>
      poly.setOptions(@hoverPolyOpts)
      @placeName.text(placepoly.previousnumber + ' ' + placepoly.name)
      @placeName.show()
      
    google.maps.event.addListener poly, 'mousemove', =>
      @placeName.css('left', mouseX)
      @placeName.css('top', mouseY)

    google.maps.event.addListener poly, 'mouseout', =>
      poly.setOptions(@currentPolyOpts)
      @placeName.hide()
