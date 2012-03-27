window.map = null
window.userPositionMarker = null

successCallback = (position) ->
  # console.log 'position', position.coords.latitude, position.coords.longitude
  $('#latitude').html(position.coords.latitude)
  $('#longitude').html(position.coords.longitude)

  pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)
  # @userPositionMarker.setPosition(pos)
  # console.log 'successCallback', userPositionMarker

  try
    window.userPositionMarker.setMap(null)

  window.userPositionMarker = new google.maps.Marker(
    icon: '/static/img/map/blue-dot.png'
    position: pos
    map: window.map
  )

  # if not userPositionMarker
  #   userPositionMarker = new google.maps.Marker(
  #     icon: '/static/img/map/blue-dot.png'
  #     position: pos
  #     map: map
  #   )
  #   #console.log 'new', userPositionMarker
  # else
  #   userPositionMarker.position = pos
  #   userPositionMarker.map = map
  #   #console.log 'existing', userPositionMarker

  window.map.setCenter(pos)


class @MapView extends Backbone.View
  events:
    #'click button#add-place': 'addPlace'
    'click #listenForPositionUpdates': '_listenForPositionUpdates'
    'click #clearWatch': '_clearWatch'

  initialize: ->
    @preferences = @options.preferences
    @nav = null
    @render()

  _clearWatch: (watchID) ->
    window.navigator.geolocation.clearWatch(watchID)
    try
      window.userPositionMarker.setMap(null)
      
    $('#listenForPositionUpdates').show()
    $('#userposition').hide()

  _listenForPositionUpdates: ->
    if not @nav
      @nav = window.navigator

    if @nav
      geoloc = @nav.geolocation
      if geoloc
        watchID = geoloc.watchPosition(successCallback)

      try
        #console.log "trying get current pos"
        geoloc.getCurrentPosition(successCallback)
        #console.log "success"

    $('#listenForPositionUpdates').hide()
    $('#userposition').show()


  addPlace: ->
    lat = window.map.getCenter().lat()
    lng = window.map.getCenter().lng()
    @places.create(territoryno: @preferences.get('territoryno'), point: "POINT (#{lat} #{lng})")

  render: ->
    window.map = new google.maps.Map @$('#map-canvas').get(0),
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
    google.maps.event.addListener window.map, 'maptypeid_changed', @onMapTypeChange

    google.maps.event.addDomListener controlUI, 'click', =>
      @addPlace()

    window.map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv)


    google.maps.event.addListener window.map, 'zoom_changed', =>
      @preferences.set('zoom', window.map.getZoom())

    @userid = @model.get('userid')
      
    if @userid > 0
      # load places
      @places = new Places()
      new PlacesView(collection: @places, map: window.map)
      new ListView(collection: @places)
      @places.fetch()

      # load boundaries
      @boundaries = new Boundaries()
      new BoundariesView(collection: @boundaries, map: window.map, preferences: @preferences)
      @boundaries.fetch()


  _togglePlaceType: (e) ->
    inputEl = @$(e.target)
    model = @collection.get(inputEl.val())
    if inputEl.is(":checked")
      model.show()
    else
      model.hide()


  # When map type changes we need to change color of polygons
  # Note:  needs fat arrow because this is used as a callback

  onMapTypeChange: =>
    switch window.map.getMapTypeId()
      when google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID
        @currentPolyOpts = @roadmapPolyOpts
      else
        @currentPolyOpts = @hybridPolyOpts
    