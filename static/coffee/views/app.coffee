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

      territoryno = @preferences.get('territoryno')
      console.log territoryno
      switch territoryno
        when "4-1-2" 
          ll = "10.001025,-84.134588"
        when "4-7-1" 
          ll = "9.98713594918928,-84.1771144239311"
        when "1-2-1" 
          ll = "9.92111127977427,-84.1474170057183"
          
      if territoryno
        @preferences.set('territoryno', territoryno)
        @preferences.set('center', ll)

        ll = ll.split(',')
        @preferences.set('centerLat', ll[0])
        @preferences.set('centerLng', ll[1])

      #console.log 'AppView preferences', @preferences

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

