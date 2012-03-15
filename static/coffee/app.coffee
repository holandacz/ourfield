#
# Set the little ajax busy loading indicator visible or not
#
showBusy = (x) ->
  if x then $('#busy').show() else $('#busy').hide()
showError = (x) ->
  if x then $('#error').show() else $('#error').hide()
  

# Tracks mouse movement in a variable

mouseX = null
mouseY = null
document.onmousemove = (e) ->
  mouseX = e.clientX
  mouseY = e.clientY

CR = "10.001025 -84.134588" # no space between


@DefaultParams =
  user_id: 0
  username: ""
  api_key: ""
  format: "json"
  limit: 0

class @AppData extends Backbone.Model
  defaults:
    center: CR
    zoom: 16
    mapTypeId: google.maps.MapTypeId.ROADMAP

  initialize: (attributes) ->

    ll = attributes.center.split(',')
    @set('centerLat', ll[0])
    @set('centerLng', ll[1])

    
    $(document).ajaxError ->
      showBusy(off)
      showError(on)


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

