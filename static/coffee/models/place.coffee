# A place has a location
class @Place extends Backbone.Model
  defaults:
    notes: ''

  # Fear the XSS.
  escapedJson: ->
    return json =
        id: @get "id"

  initialize: (attributes) ->
    match = attributes.point?.match(/(\-?\d+(?:\.\d+)?)\s(\-?\d+(?:\.\d+)?)/)
    if match?
      @set('lat', match[1])
      @set('lng', match[2])

    params = {}
    params = $.param(_.defaults(params, DefaultParams))
    if @has('resource_uri')
      @url = @get('resource_uri') + "?#{params}"

    @bind 'change', @recalcPoint

  recalcPoint: =>
    if @hasChanged('lat') or @hasChanged('lng')
      lat = @get('lat')
      lng = @get('lng')
      @set('point', "POINT(#{lat} #{lng})")

  toJSON: ->
    deleted: @get('deleted')
    googlemapurl: @get('googlemapurl')
    point: @get('point')
    territoryno: @get('territoryno') 
    routemarkernoafter: @get('routemarkernoafter')
    markerno: @get('markerno')
    #blockno: @get('blockno')
    name: @get('name')
    houseno: @get('houseno')
    description: @get('description')
    #languages: @get('languages')
    persons: @get('persons')
    phonenos: @get('phonenos')
    emails: @get('emails')
    tonext: @get('tonext')
    notes: @get('notes')
    interestlevel: @get('interestlevel')
    actions: @get('actions')

