// global ofmap object
var ofmap = {
    explore: {
        items: {}
    },
    rating: {}
};


ofmap.createBasemap = function (mapdiv) {
    ofmap.map = new google.maps.Map(document.getElementById(mapdiv));

    // simple map style
    var simple_style =  [
        {
            featureType: "administrative",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "administrative",
            elementType: "labels",
            stylers: [
                { visibility: "on" },
                { hue: "#d70000" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        },{
            featureType: "landscape",
            elementType: "all",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "geometry",
            stylers: [
                { visibility: "off" }
            ]
        },{
            featureType: "poi",
            elementType: "labels",
            stylers: [
                { visibility: "on" },
                { hue: "#d70000" },
                { lightness: 10 },
                { saturation: -95 }
            ]
        }
    ];

    var simple_options = {
        name: "Simple"
    }

    var simple = new google.maps.StyledMapType(simple_style, simple_options);


    ofmap.map.mapTypes.set("simple", simple);
    ofmap.map.setMapTypeId("simple");
    ofmap.map.streetViewControl = false;
    ofmap.map.setOptions({
        mapTypeControlOptions: {
            position: google.maps.ControlPosition.TOP_RIGHT,
            mapTypeIds: ["simple",google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.SATELLITE],
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
        },
        panControl: false,
        zoomControlOptions: {
            style: google.maps.ZoomControlStyle.SMALL
        },
    });

    // map icons
    ofmap.icons = {
        'shadow': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/shadow.png',
            new google.maps.Size(51,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'dot_red': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/dot_red.png',
            new google.maps.Size(6,6),
            new google.maps.Point(0,0),
            new google.maps.Point(3,6)
        ),
        'dot_green': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/dot_green.png',
            new google.maps.Size(6,6),
            new google.maps.Point(0,0),
            new google.maps.Point(3,6)
        ),
        // station icon
        'station': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/train.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'i': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/idea.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'm': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/text.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'n': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/text.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'e': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/photo.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'photo': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/photo.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'video': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/video.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        ),
        'd': new google.maps.MarkerImage(ofmap.static_url + 'img/isicons/chart.png',
            new google.maps.Size(32,37),
            new google.maps.Point(0,0),
            new google.maps.Point(16,37)
        )
    };
}

// render places
ofmap.createPlaceMarker = function (options) {
    var s_ll = new google.maps.LatLng(options.lat,options.lon);
    var marker = new google.maps.Marker({
        position: s_ll, 
        map: ofmap.map,
        draggable: true,
        title: options.title,
        id: options.id,
        //shadow: ofmap.icons['shadow'],
        icon: ofmap.icons['dot_green'],
        zIndex: 0
    });
    
      // Add dragging event listeners.
    google.maps.event.addListener(marker, 'dragstart', function() {
        updateMarkerAddress('Dragging...');
    });
    
    google.maps.event.addListener(marker, 'drag', function() {
        updateMarkerStatus('Dragging...');
        updateMarkerPosition(marker.getPosition());
    });
    
    google.maps.event.addListener(marker, 'dragend', function() {
        pos = marker.getPosition();
        geocodePosition(pos);
        $.post('/places/post_test/' , {id:marker.id, lat:pos.lat(), lng:pos.lng()});
        updateMarkerStatus('Drag ended');
        
    });
    
}

// render station markers
ofmap.createEnMarker = function (options) {
    var s_ll = new google.maps.LatLng(options.lat,options.lon);
    var s_marker = new google.maps.Marker({
        position: s_ll, 
        map: ofmap.map,
        title: options.title,
        //shadow: ofmap.icons['shadow'],
        icon: ofmap.icons['dot_red'],
        zIndex: 0
    });
}


// render ofmap
ofmap.createPoly = function (options) {
    var poly = new google.maps.Polygon({
        path: google.maps.geometry.encoding.decodePath(options.points),
        levels: ofmap.decodeLevels(options.levels),
        strokeColor: '#4F7B41',
        strokeOpacity: 0.9,
        strokeWeight: 1,
        zoomFactor: options.zoomFactor, 
        numLevels: options.numLevels,
        map: ofmap.map
    });
}



// requires 3rd party infobubble lib http://google-maps-utility-library-v3.googlecode.com/svn/trunk/infobubble/
ofmap.createInfoBubble = function (type, marker, contentstring) {
    google.maps.event.addListener(marker, 'click', function() {
        ofmap.infobubble[type].setContent(contentstring);
        ofmap.infobubble[type].open(ofmap.map, marker);
    });
}

ofmap.decodeLevels = function (encodedLevelsString) {
    var decodedLevels = [];
    for (var i = 0; i < encodedLevelsString.length; ++i) {
        var level = encodedLevelsString.charCodeAt(i) - 63;
        decodedLevels.push(level);
    }
    return decodedLevels;
}

// load shared items for explore page
ofmap.explore.loadItems = function () {
    // update filter options
    var filter = {
        bbox: ofmap.map.getBounds().toUrlValue(4),
        };
    // load data
    $.getJSON('/map/items/',
        filter,
        function(data) {
            // add new markers to map
            $.each(data, function(i,item){
                if (ofmap.explore.items[i] === undefined) {
                    ofmap.explore.items[i] = new google.maps.Marker({
                    position: new google.maps.LatLng(item.lat, item.lon), 
                        map: ofmap.map,
                            title: item.title,
                                shadow: ofmap.icons['shadow'],
                                icon: ofmap.icons[item.itemtype],
                                zIndex: 1
                                });
                                }
                                });
                            });
                        }
                
    






















