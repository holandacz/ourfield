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

