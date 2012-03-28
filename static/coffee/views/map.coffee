window.map = null
window.userPositionMarker = null

successCallback = (position) ->
  console.log 'position', position.coords.latitude, position.coords.longitude
  if position.coords.latitude
    $('#userpositionlatlng').show()

    $('#userpositionlat').html(position.coords.latitude)
    $('#userpositionlng').html(position.coords.longitude)

    pos = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)

    try
      window.userPositionMarker.setMap(null)

    switch window.map.getMapTypeId()
      when google.maps.MapTypeId.ROADMAP
        icon = '/static/img/map/blue-dot.png'
      else
        icon = '/static/img/map/white-dot.png'

    window.userPositionMarker = new google.maps.Marker(
      icon: icon
      position: pos
      map: window.map
      title: 'You are here.'
    )

    window.map.setCenter(pos)

geolocationError = (error) ->
  msg = 'Unable to locate position. '
  switch error.code
    when error.TIMEOUT then msg += 'Timeout.'
    when error.POSITION_UNAVAILABLE then msg += 'Position unavailable.'
    when error.PERMISSION_DENIED then msg += 'Please turn on location services.'
    when error.UNKNOWN_ERROR then msg += error.code
  $('.alert-message').remove()
  alert = $('<div class="alert-message error fade in" data-alert="alert">')
  alert.html('<a class="close" href="#">×</a>' + msg);
  alert.insertBefore($('.span10'))

class @MapView extends Backbone.View
  events:
    'click #listenForPositionUpdates': '_listenForPositionUpdates'
    'click #cancelTrack': '_cancelTrack'
    'click #addPlace': 'addPlace'
    'click #gotoHome': 'gotoHome'

  initialize: ->
    @preferences = @options.preferences
    @nav = null
    @render()

  _cancelTrack: (watchID) ->
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
        watchID = geoloc.watchPosition(successCallback, geolocationError, options={enableHighAccuracy: true})

      try
        geoloc.getCurrentPosition(successCallback, geolocationError, options={enableHighAccuracy: true})

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
      draggableCursor: 'default'
      draggingCursor: 'pointer'
      mapTypeControl: true
      
      mapTypeControlOptions: 
        # style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        mapTypeIds: [google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID]


    # google.maps.event.addListener @map, 'idle', @onIdle
    google.maps.event.addListener window.map, 'maptypeid_changed', @onMapTypeChange

    google.maps.event.addListener window.map, 'zoom_changed', =>
      @preferences.set('zoom', window.map.getZoom())

    google.maps.event.addListener window.map, 'center_changed', @onMapCenterChanged

    @userid = @model.get('userid')

    @onMapCenterChanged()

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

  onMapCenterChanged: =>
    lat = window.map.getCenter().lat()
    lng = window.map.getCenter().lng()
    $('#crosshairlat').html(lat)
    $('#crosshairlng').html(lng)


  gotoHome: =>
    window.location = "#home"

  onMapTypeChange: =>
    switch window.map.getMapTypeId()
      when google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID
        @currentPolyOpts = @roadmapPolyOpts
      else
        @currentPolyOpts = @hybridPolyOpts
    