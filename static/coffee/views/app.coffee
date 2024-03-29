
# # Gets the users current position
# # navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options)
# navigator.geolocation.getCurrentPosition()

# # Request repeated updates of position
# # watchId = navigator.geolocation.watchPosition(successCallback, errorCallback)
# watchId = navigator.geolocation.watchPosition()

# # Cancel the updates
# # navigator.geolocation.clearWatch(watchId)
# navigator.geolocation.clearWatch()

class @AppView extends Backbone.View

  initialize: ->
    @preferences = @options.preferences

    # @getGeolocation()

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
          pageheader = "1-2-1 San Jose/Escazu/Escazu/West"
        when "1-2-2" 
          ll = "9.92111127977427,-84.1474170057183"
          zoom = 14
          pageheader = "1-2-2 San Jose/Escazu/Escazu/East"
        when "1-2-3 (A)" 
          ll = "9.93246946647039,-84.1332120267754"
          zoom = 17
          pageheader = "1-2-3 (A) San Jose/Escazu/San Rafael/A"
        when "1-2-3 (B)" 
          ll = "9.93162666503805,-84.1328338353043"
          zoom = 17
          pageheader = "1-2-3 (B) San Jose/Escazu/San Rafael/B"
        when "1-2-3 (3)" 
          ll = "9.93138888367707,-84.1331557003861"
          zoom = 17
          pageheader = "1-2-3 (3) San Jose/Escazu/San Rafael/3"
        when "1-2-3 (10)" 
          ll = "9.93138888367707,-84.1331557003861"
          zoom = 17
          pageheader = "1-2-3 (10) San Jose/Escazu/San Rafael/3"
        when "4-1-2" 
          ll = "10.001025,-84.134588"
          pageheader = "4-1-2 Heredia/Heredia/Mercedes"
          zoom = 15

        when "4-7-1" 
          ll = "9.98713594918928,-84.1771144239311"
          zoom = 15
          pageheader = "4-7-1 Heredia/Belen/La Ribera/La Ribera-San Antonio de Belen"

        when "4-7-3 (A)" 
          ll = "9.98713594918928,-84.1771144239311"
          zoom = 17
          pageheader = "4-7-3 (A) Heredia/Asuncion/Cariari/Cariari"

        when "4-7-3" 
          ll = "9.970288,-84.156647"
          zoom = 17
          pageheader = "4-7-3 Heredia/Asuncion/Cariari/Ciudad Cariari"

        when "BS" 
          ll = "9.984336,-84.168733"
          zoom = 14
          pageheader = "Belen Sur"

        when "BSP" 
          ll = "9.832594,-83.863235"
          zoom = 15
          pageheader = "Belen Sur Paraiso"

        when "BSZ" 
          ll = "10.1843,-84.40002"
          zoom = 14
          pageheader = "Belen Sur Zarcero"


        when "999" 
          ll = "9.98713594918928,-84.1771144239311"
          zoom = 13
          pageheader = "999 Unassigned"

      $('.page-header').html(pageheader)
      $('#territory-menu').html(territoryno + '<b class="caret"></b>')

      if territoryno
        @preferences.set('territoryno', territoryno)
        #@preferences.set('center', ll)
        @preferences.set('zoom', zoom)
      else
        @preferences.set('zoom', 13)
        ll = "9.981192,-84.185314" # Belen English CR
        #@preferences.set('center', ll)

      ll = ll.split(',')
      @preferences.set('centerLat', ll[0])
      @preferences.set('centerLng', ll[1])



      # coords = new google.maps.LatLng(position.coords.latitude, position.coords.longitude)

      # marker = new google.maps.Marker
      #   position: coords
      #   map: @mapView.map
      #   title:"You are here!"



    @searchView = new SearchView
      el: '#search'
      model: @model
      preferences: @preferences

