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

    @userid = @model.get('userid')



      # window.placeTypes.models[0].places.add({id:3, point: 'POINT (10.001 -84.134)'})
      # make into a function: @addPlace(event)

    # google.maps.event.addListener @map, "click", => @addPlace()
    # location: event.latLng
    # centered: false

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

    # LWE added to try to refresh inforwindow
    @model.bind 'sync', @show
    @render()

  render: ->
    @position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))

    title = 'P' + @model.get('id')
    if @model.get('interestlevel')
      title += " - INTEREST " + @model.get('interestlevel')

    if @model.get('territoryno')
      title += " - TERRITORY# " + @model.get('territoryno')

    if @model.get('markerno')
      title += " - MARKER# " + @model.get('markerno')

    if @model.get('sortno')
      title += " - SORT# " + @model.get('sortno')

    if @model.get('blockno')
      title += " - BLOCK# " + @model.get('blockno')

    if @model.get('houseno')
      title += " - HOUSE# " + @model.get('houseno')

    if @model.get('description')
      title += "\n\n" + "DESCRIPTION\n" + @model.get('description')

    # code to show languages with a number in front of language code

    if @model.get('persons')
      title += "\n\n" + "PERSONS\n" + @model.get('persons')

    if @model.get('actions')
      title += "\n\n" + "ACTIONS\n" + @model.get('actions')

    if @model.get('notes')
      title += "\n\n" + "NOTES\n" + @model.get('notes')



    @marker = new google.maps.Marker(
      position: @position
      draggable: true
      #animation: google.maps.Animation.DROP
      title: title
    )

    # @infoWindow = new InfoWindow(map: @map, marker: @marker, model: @model)

    google.maps.event.addListener @marker, "dragend", @dragend
    google.maps.event.addListener @marker, "click", @click

    @show()

  dragend: =>
    if confirm("Are you sure you want to move this marker?")
      @model.set(lat:  @marker.position.lat(), lng: @marker.position.lng())
      @model.save()
    else
      # move back to original position
      @marker.position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))
      @marker.setMap(@map)

  show: =>
    @marker.setMap(@map)

  hide: =>
    @marker.setMap(null)

  click: =>
    @infoWindow = new InfoWindow(model: @model)

class InfoWindow extends Backbone.View
  template: _.template($('#info-window-template').html())

  editTemplate: _.template($('#edit-info-window-template').html())

  className: 'modal'

  events:
    'click a.edit': '_edit'
    'click a.view': '_view'
    'click a.save-continue': '_saveContinue'
    'click a.save': '_save'

  initialize: ->
    @editing = false
    @render()

  render: ->
    if @editing
      @$el.html(@editTemplate(model: @model))
    else
      @$el.html(@template(model: @model))
    @$el.modal('show')

  _edit: ->
    @editing = true
    @render()

  _view: ->
    if confirm("Are you sure you want to abandon edit?")
      @editing = false
      @render()

  _saveContinue: ->
    @persist()

  _save: ->
    @persist()
    @model.bind 'sync', =>
      @$el.modal('hide')

  persist: ->
    @model.set
      territoryno: @$('#ed-territoryno').val()
      markerno: (Number) @$('#ed-markerno').val()
      sortno: (Number) @$('#ed-sortno').val()
      blockno: @$('#ed-blockno').val()
      interestlevel: (Number) @$('#ed-interestlevel').val()
      houseno: @$('#ed-houseno').val()
      description: @$('#ed-description').val()
      languages: @$('#ed-languages').val()
      persons: @$('#ed-persons').val()
      notes: @$('#ed-notes').val()
      actions: @$('#ed-actions').val()
    @model.save()
