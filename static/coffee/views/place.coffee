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
    @placeItemViews.push(new PlaceItemView(collection: @collection, model: place, map: @map))

class @PlaceItemView extends Backbone.View
  initialize: ->
    @map = @options.map
    @collection = @options.collection
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

    title = ''

    routemarkernoafter = @model.get('routemarkernoafter')
    if routemarkernoafter
      title += (' Route AFTER #' + routemarkernoafter)




    title += ' ' + @model.get('markerno')
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

      if @model.get('interestlevel')
        @marker.setIcon('/static/img/mapicons/25x30/green/numbers/number_' +  @model.get('markerno') + '.png')
      else
        @marker.setIcon('/static/img/mapicons/25x30/white/numbers/number_' +  @model.get('markerno') + '.png')
    else
      @marker.setIcon('/static/img/mapicons/25x30/white/symbol_blank.png')
    
    @marker.setMap(@map)

  hide: =>

    @marker.setMap(null)

  click: =>
    @infoWindow = new InfoWindow(collection: @collection, model: @model)

class InfoWindow extends Backbone.View

  template: _.template($('#info-window-template').html())

  editTemplate: _.template($('#edit-info-window-template').html())

  className: 'modal'

  events:
    'click a.route': '_route'
    'click a.delete': '_delete'
    'click a.edit': '_edit'
    'click a.view': '_view'
    'click a.save-continue': '_saveContinue'
    'click a.save': '_save'

  initialize: ->
    @collection = @options.collection
    @editing = @options.editing || false
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



  _route: ->
    if not confirm("Are you sure you want to route from this place?")
      return

    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    $.get '/places/route/' +  @model.get('id') + '/?' + params, (data) =>
      console.log data


    @persist()
    @model.bind 'sync', =>
      @$el.modal('hide')
      
    # @collection.fetch()
    # @$el.modal('hide')
    # @render()


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
      googlemapurl: @$('#ed-googlemapurl').val()
      territoryno: @$('#ed-territoryno').val()
      routemarkernoafter: (Number) @$('#ed-routemarkernoafter').val()
      markerno: (Number) @$('#ed-markerno').val()
      blockno: @$('#ed-blockno').val()
      interestlevel: (Number) @$('#ed-interestlevel').val()
      name: @$('#ed-name').val()
      houseno: @$('#ed-houseno').val()
      description: @$('#ed-description').val()
      languages: @$('#ed-languages').val()
      persons: @$('#ed-persons').val()
      phonenos: @$('#ed-phonenos').val()
      emails: @$('#ed-emails').val()
      notes: @$('#ed-notes').val()
      actions: @$('#ed-actions').val()
      tonext: @$('#ed-tonext').val()
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
  events:
    'click .list-id': '_clickid'

  initialize: ->
    @render()

  render: ->
    $('#list').append(@el)

    html = ''
    html += '<div class="list-item-row" id="list-item-row-' + @model.get('id') + '">'


    if @model.get('interestlevel')
      html += '<img class="list-marker" src="/static/img/mapicons/25x30/green/numbers/number_' + @model.get('markerno') + '.png" />'
    else
      html += '<img class="list-marker" src="/static/img/mapicons/25x30/white/numbers/number_' + @model.get('markerno') + '.png" />'



    if @model.get('multiunit')
      html += '&nbsp;&nbsp;<span class="list-multiunit">MultiUnit</span>'

    if not @model.get('residential')
      html += '&nbsp;&nbsp;<span class="list-residential">BIZ</span>'

    # if not @model.get('confirmed')
    #   html += '&nbsp;&nbsp;<span class="list-confirmed">?</span>'



    html += '&nbsp;&nbsp;<span class="list-id">p' + @model.get('id') + '</span>'



    # if @model.get('interestlevel')
    #   html += '<span class="list-title list-interestlevel">INTEREST</span>'

    if @model.get('name') or @model.get('houseno') or @model.get('directions') or @model.get('description')
      html += '<span class="list-title list-title">ADDRESS:</span>'
      if @model.get('name') 
        html += '<span class="list-row-text list-name">' + @model.get('name') + '</span>&nbsp;'
      if @model.get('houseno') 
        html += '<span class="list-row-text list-houseno">' + @model.get('houseno') + '</span>&nbsp;'
      if @model.get('directions')          
        html += '<span class="list-row-text list-directions">' + @model.get('directions') + '</span>&nbsp;'
      if @model.get('description')          
        html += '<span class="list-row-text list-description">' + @model.get('description') + '</span>&nbsp;'

    if @model.get('persons')
      html += '<span class="list-title list-title">PERSON(S):</span>'
      html += '<span class="list-row-text list-persons">' + @model.get('persons') + '</span>'

    if @model.get('phonenos')
      html += '<span class="list-title list-title">PHONE(S):</span>'
      html += '<span class="list-row-text list-phonenos">' + @model.get('phonenos') + '</span>'

    if @model.get('emails')
      html += '<span class="list-title list-title">EMAIL(S):</span>'
      html += '<span class="list-row-text list-emails">' + @model.get('emails') + '</span>'

    if @model.get('notes')
      html += '<span class="list-title list-title">NOTES:</span>'
      html += '<span class="list-row-text list-notes">' + @model.get('notes') + '</span>'

    if @model.get('actions')
      html += '<div class="list-item-actions" id="list-actions-' + @model.get('id') + '">'
      html += '<span class="list-title list-title">ACTIONS:</span>'
      html += '<span class="list-row-text list-actions">' + @model.get('actions') + '</span>'
      html += '</div>'


    if @model.get('tonext')
      html += '<span class="list-title list-title">&#187; TO NEXT:</span>'
      html += '<span class="list-row-text list-tonext">' + @model.get('tonext') + '</span>'

    html += '</div>'

    #$('#list').append(html)
    @$el.html(html)


  _clickid: ->
    console.log 'clickid'
    @infoWindow = new InfoWindow(model: @model, editing: true)

class @LogView extends Backbone.View
  initialize: ->
    Log.on 'log', (message) ->
      $('#log').append("<div>#{message}</div>")

    @render()

  render: ->

class @SearchView extends Backbone.View
  # initilaize: ->
  #   @render()

  # render: ->