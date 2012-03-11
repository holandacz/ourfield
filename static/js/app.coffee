class @Preferences
  constructor: ->
    @cookieName = "preferences"
    @items = {}
    @load()

  load: ->
    rawValue = $.cookie(@cookieName)
    if rawValue
      @items = JSON.parse(rawValue)

  save: ->
    $.cookie(@cookieName, JSON.stringify(@items), expires: 365)

  get: (key) ->
    @items[key]

  set: (key, value) ->
    @items[key] = value
    @save()

  setDefault: (key, defaultValue) ->
    @items[key] = defaultValue unless @items[key]
    @save()

@Log =
  log: (message) ->
    @trigger 'log', message

_.extend(@Log, Backbone.Events)

class @AppView extends Backbone.View
  initialize: ->
    @preferences = @options.preferences
    @collection.bind 'sync', => 
      @collection.fetch()
    @render()

  render : ->
    @mapView = new MapView
      el: '#map'
      model: @model
      collection: @collection
      preferences: @preferences

    @listView = new ListView
      el: '#list'
      model: @model
      collection: @collection.get(1).places
      preferences: @preferences

    # @logView = new LogView 
    #   el: '#log'

    @searchView = new SearchView
      el: '#search'
      model: @model
      collection: @collection
      preferences: @preferences

class @MapView extends Backbone.View
  events:
    'click input[type="checkbox"]': '_togglePlaceType'
    'click button#add-place': '_addPlace'

  initialize: ->
    @preferences = @options.preferences
    @render()

  render: ->
    console.log @preferences.items

    @map = new google.maps.Map @$('#map-canvas').get(0),
      zoom: @preferences.get('zoom')
      center: new google.maps.LatLng(@model.get('centerLat'), @model.get('centerLng'))
      mapTypeId: @model.get('mapTypeId')

    google.maps.event.addListener @map, 'zoom_changed', =>
      @preferences.set('zoom', @map.getZoom())

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
    console.log lat, lng
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
    # @collection.bind 'sync', =>
    #   @collection.fetch()
    @collection.bind 'reset', @render
    @render() if @collection.length > 0

  render: =>
    _.each @placeItemViews, (placeItemView) =>
      placeItemView.hide()
    @placeItemViews = []
    @collection.each @addPlaceItemView

  addPlaceItemView: (place) =>
    place.bind 'sync', =>
      @collection.fetch()
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
    @marker = new google.maps.Marker(
      draggable: true
    )

    google.maps.event.addListener @marker, "dragend", @dragend
    google.maps.event.addListener @marker, "click", @click

    @show()

  dragend: =>
    if confirm("Are you sure you want to move this marker?")
      @model.set(lat:  @marker.position.lat(), lng: @marker.position.lng())
      @model.save()
      Log.log('dragged')
      # get newMarkerno(asadsasdf)
    else
      # move back to original position
      @marker.setPosition( new google.maps.LatLng(@model.get('lat'), @model.get('lng')))

  show: =>
    @position = new google.maps.LatLng(@model.get('lat'), @model.get('lng'))
    @marker.setPosition(@position)

    title = @model.get('markerno')
    title += ' p' + @model.get('id')

    if @model.get('interestlevel')
      title += " INTERESTED! "

    if @model.get('houseno') or @model.get('description')
      title += "  ADDR: " + @model.get('houseno')
      title += @model.get('description')

    if @model.get('persons')
      title += " " + "PERSONS: " + @model.get('persons')

    if @model.get('notes')
      title += " " + "NOTES: " + @model.get('notes')

    if @model.get('actions')
      title += " " + "ACTIONS: " + @model.get('actions')


    @marker.setTitle(title)

    if @model.get('markerno')
      @marker.setIcon('/site_media/static/img/mapicons/25x30/numbers/number_' +  @model.get('markerno') + '.png')
    else
      @marker.setIcon('/site_media/static/img/mapicons/25x30/symbol_blank.png')
    
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
    'click a.delete': '_delete'
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

  _delete: ->
    if confirm("Are you sure you want to delete this place?")
      @model.bind 'destroy', =>
        @$el.modal('hide')
      @model.destroy()

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
      blockno: @$('#ed-blockno').val()
      interestlevel: (Number) @$('#ed-interestlevel').val()
      houseno: @$('#ed-houseno').val()
      description: @$('#ed-description').val()
      languages: @$('#ed-languages').val()
      persons: @$('#ed-persons').val()
      notes: @$('#ed-notes').val()
      actions: @$('#ed-actions').val()
    @model.save()

class @ListView extends Backbone.View
  initialize: ->
    @collection.bind 'reset', @render
    @collection.bind 'add', @addListItemView
    @render() if @collection.length > 0

  render: =>
    $('#list').empty()
    @collection.each @addListItemView

  addListItemView: (model) =>
    new ListItemView(model: model)

class @ListItemView extends Backbone.View
  # events:
  #   'click #list-id-': '_clickid'

  initialize: ->
    @render()

  render: ->
    $('#list').append(@el)

    html = ''
    html += '<div class="list-item-row" id="list-item-row-' + @model.get('id') + '">'
    html += '<img src="/site_media/static/img/mapicons/25x30/numbers/number_' + @model.get('markerno') + '.png" />'

    if @model.get('multiunit')
      html += '&nbsp;&nbsp;<span class="list-multiunit">MultiUnit</span>'

    if not @model.get('residential')
      html += '&nbsp;&nbsp;<span class="list-residential">BIZ</span>'

    if not @model.get('confirmed')
      html += '&nbsp;&nbsp;<span class="list-confirmed">?</span>'

    html += '&nbsp;&nbsp;<span class="list-id" id="list-id-' + @model.get('id') + '">p' + @model.get('id') + '</span>'

    if @model.get('interestlevel')
      html += '<span class="list-title list-interestlevel">INTEREST</span>'

    if @model.get('houseno') or @model.get('directions') or @model.get('description')
      html += '<span class="list-title list-title">ADDRESS:</span>'
      if @model.get('houseno') 
        html += '<span class="list-houseno">' + @model.get('houseno') + '</span>&nbsp;'
      if @model.get('directions')          
        html += '<span class="list-directions">' + @model.get('directions') + '</span>&nbsp;'
      if @model.get('description')          
        html += '<span class="list-description">' + @model.get('description') + '</span>&nbsp;'

    if @model.get('persons')
      html += '<span class="list-title list-title">PERSON(S):</span>'
      html += '<span class="list-persons">' + @model.get('persons') + '</span>'

    if @model.get('notes')
      html += '<span class="list-title list-title">NOTES:</span>'
      html += '<span class="list-notes">' + @model.get('notes') + '</span>'

    if @model.get('actions')
      html += '<div class="list-item-actions" id="list-actions-' + @model.get('id') + '">'
      html += '<span class="list-title list-title">ACTIONS:</span>'
      html += '<span class="list-actions">' + @model.get('actions') + '</span>'
      html += '</div>'


    html += '</div>'

    $('#list').append(html)


  # clickid: =>
  #   console.log 'clickid'
  #   #@infoWindow = new InfoWindow(model: @model)

class @LogView extends Backbone.View
  initialize: ->
    Log.on 'log', (message) ->
      $('#log').append("<div>#{message}</div>")

    @render()

  render: ->

class @SearchView extends Backbone.View
  initilaize: ->
    @render()

  render: ->