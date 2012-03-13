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

