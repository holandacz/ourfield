class @AppView extends Backbone.View
  initialize: ->
    @preferences = @options.preferences
    # @placeTypes = @options.placeTypes
    # @boundaries = @options.boundaries

    # @placeTypes.bind 'sync', => 
    #   @placeTypes.fetch()

    # @boundaries.bind 'sync', => 
    #   @boundaries.fetch()

    @render()

  render : ->
    @mapView = new MapView
      el: '#map'
      model: @model
      # collection: @placeTypes
      # boundaries: @boundaries
      preferences: @preferences
      
      #@boundaries.fetch()
      #console.log @boundaries


      territoryno = @preferences.get('territoryno')
      zoom = @preferences.get('zoom')
      switch territoryno
        when "1-2-1" 
          ll = "9.92111127977427,-84.1474170057183"
          zoom = 14
          pageheader = "San Jose/Escazu/Escazu/West"
        when "1-2-2" 
          ll = "9.92111127977427,-84.1474170057183"
          zoom = 14
          pageheader = "San Jose/Escazu/Escazu/East"
        when "4-1-2" 
          ll = "10.001025,-84.134588"
          pageheader = "Heredea/Heredia/Mercedes"
          zoom = 17
        when "4-7-1" 
          ll = "9.98713594918928,-84.1771144239311"
          zoom = 15
          pageheader = "Heredea/Belen/La Ribera/La Ribera-San Antionio de Belen"
        when "4-7-3" 
          ll = "9.970288,-84.156647"
          zoom = 17
          pageheader = "Heredea/Asuncion/Cariari/Ciudad Cariari"
        when "999" 
          ll = "9.98713594918928,-84.1771144239311"
          zoom = 13
          pageheader = "Unassigned"

      $('.page-header').html(pageheader)

      if territoryno
        @preferences.set('territoryno', territoryno)
        @preferences.set('center', ll)
        @preferences.set('zoom', zoom)
      else
        @preferences.set('zoom', 13)
        ll = "9.981192,-84.185314" # Belen English CR
        @preferences.set('center', ll)

      ll = ll.split(',')
      @preferences.set('centerLat', ll[0])
      @preferences.set('centerLng', ll[1])


    # console.log 'mapView.boundaries', @mapView.boundaries
    #console.log 'territoryno', @preferences.get('territoryno')

    #poly = @mapView.polys[652]

    # console.log 'mapView', @mapView
    # console.log 'mapView.polys', @mapView.polys

    #console.log 'poly', poly

    # if @preferences.get('territoryno') == '4-1-2'
    #   poly = @mapView.polys[652]
    #   console.log 'poly', poly

    # @logView = new LogView 
    #   el: '#log'

    @searchView = new SearchView
      el: '#search'
      model: @model
      preferences: @preferences

