class @MapView extends Backbone.View
  events:
    'click input[type="checkbox"]': '_togglePlaceType'
    'click button#add-place': '_addPlace'

  initialize: ->
    @render()


  render: ->
    @map = new google.maps.Map @$('#map-canvas').get(0),
      zoom: @model.get('zoom')
      center: new google.maps.LatLng(@model.get('centerLat'), @model.get('centerLng'))
      mapTypeId: @model.get('mapTypeId')



      # window.placeTypes.models[0].places.add({id:3, point: 'POINT (10.001 -84.134)'})
      # make into a function: @addPlace(event)

    # google.maps.event.addListener @map, "click", => @addPlace()
    # location: event.latLng
    # centered: false



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

  _addPlace: (e) ->
    console.log "_addPlace", e
    lat = @map.getCenter().lat()
    lng = @map.getCenter().lng()
    @collection.get(1).places.create(point: "POINT (#{lat} #{lng})")


class @PlaceTypeView extends Backbone.View
  initialize: ->
    @map = @options.map
    @model.bind 'show', @show
    @model.bind 'hide', @hide
    @render()

  render: ->
    @placesView = new PlacesView(collection: @collection, map: @map)

  show: =>
    @collection.fetch()

  hide: =>

class @PlacesView extends Backbone.View
  initialize: ->
    @map = @options.map
    @placeItemViews = []
    @collection.bind 'add', @addPlaceItemView
    @collection.bind 'reset', @render
    @render() if @collection.length > 0

  render: =>
    _.each @placeItemViews, (placeItemView) =>
      placeItemView.hide()
    @collection.each @addPlaceItemView

  addPlaceItemView: (place) =>
    @placeItemViews.push(new PlaceItemView(model: place, map: @map))

class @PlaceItemView extends Backbone.View
  initialize: ->
    @map = @options.map
    @model.bind 'show', @show
    @model.bind 'hide', @hide
    @render()

  render: ->
    @position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))

    @marker = new google.maps.Marker(
      position: @position
      draggable: true
      animation: google.maps.Animation.DROP
      title: @position.lat() + "," + @position.lng()
    )

    @infoWindow = new InfoWindow(map: @map, marker: @marker, model: @model)

    google.maps.event.addListener @marker, "dragend", @dragend
    google.maps.event.addListener @marker, "click", @click

    @show()

  dragend: =>
    @model.set(lat:  @marker.position.lat(), lng: @marker.position.lng())
    @model.save()

  show: =>
    @marker.setMap(@map)

  hide: =>
    @marker.setMap(null)

  click: =>
    console.log "PlaceItemView#click"
    @infoWindow.show()

class @InfoWindow extends Backbone.View
  template: _.template($('#info-window-template').html())

  events:
    'click button.edit': '_edit'

  initialize: ->
    @map = @options.map
    @marker = @options.marker
    @render()

  render: ->
    @window = new google.maps.InfoWindow
      maxWidth: 350
    google.maps.event.addListener @window, 'domready', @domReady

  show: ->
    @templateParams =
      id: _.uniqueId('info-window-')
      model: @model
    @window.setContent(@template(@templateParams))
    @window.open(@map, @marker)

  hide: ->
    @window.close()

  domReady: =>
    @setElement($('#' + @templateParams.id))

  _edit: ->
    @editInfoWindow = new EditInfoWindow(model: @model)

class EditInfoWindow extends Backbone.View
  template: _.template($('#edit-info-window-template').html())

  className: 'modal'

  events:
    'click a.save': '_save'

  initialize: ->
    @render()

  render: ->
    @$el.html(@template(model: @model))
    @$el.modal('show')

  _save: ->
    @model.set
      notes: @$('textarea').val()
    @model.save()
