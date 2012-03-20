// Generated by CoffeeScript 1.2.1-pre
(function() {
  var CR, InfoWindow, mouseX, mouseY, showBusy, showError,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  this.Boundary = (function(_super) {

    __extends(Boundary, _super);

    Boundary.name = 'Boundary';

    function Boundary() {
      return Boundary.__super__.constructor.apply(this, arguments);
    }

    Boundary.prototype.escapedJson = function() {
      var json;
      return json = {
        id: this.get("id")
      };
    };

    Boundary.prototype.initialize = function(attributes) {
      var latlngs, match, params, point, points, _ref;
      match = (_ref = attributes.poly) != null ? _ref.match(/(-?\d+(?:\.\d+)?)\s(-?\d+(?:\.\d+)?)/mg) : void 0;
      if (match != null) {
        points = (function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = match.length; _i < _len; _i++) {
            point = match[_i];
            _results.push(point.split(' '));
          }
          return _results;
        })();
        latlngs = (function() {
          var _i, _len, _results;
          _results = [];
          for (_i = 0, _len = points.length; _i < _len; _i++) {
            point = points[_i];
            _results.push(new google.maps.LatLng(point[1], point[0]));
          }
          return _results;
        })();
        this.set('latlngs', latlngs);
      }
      this.id = attributes.id;
      this.cid = attributes.previousnumber;
      params = {};
      params = $.param(_.defaults(params, DefaultParams));
      if (this.has('resource_uri')) {
        return this.url = this.get('resource_uri') + ("?" + params);
      }
    };

    Boundary.prototype.toJSON = function() {
      return {
        poly: this.get('poly')
      };
    };

    return Boundary;

  })(Backbone.Model);

  this.Place = (function(_super) {

    __extends(Place, _super);

    Place.name = 'Place';

    function Place() {
      this.recalcPoint = __bind(this.recalcPoint, this);
      return Place.__super__.constructor.apply(this, arguments);
    }

    Place.prototype.defaults = {
      notes: ''
    };

    Place.prototype.escapedJson = function() {
      var json;
      return json = {
        id: this.get("id")
      };
    };

    Place.prototype.initialize = function(attributes) {
      var match, params, _ref;
      match = (_ref = attributes.point) != null ? _ref.match(/(\-?\d+(?:\.\d+)?)\s(\-?\d+(?:\.\d+)?)/) : void 0;
      if (match != null) {
        this.set('lat', match[1]);
        this.set('lng', match[2]);
      }
      params = {};
      params = $.param(_.defaults(params, DefaultParams));
      if (this.has('resource_uri')) {
        this.url = this.get('resource_uri') + ("?" + params);
      }
      return this.bind('change', this.recalcPoint);
    };

    Place.prototype.recalcPoint = function() {
      var lat, lng;
      if (this.hasChanged('lat') || this.hasChanged('lng')) {
        lat = this.get('lat');
        lng = this.get('lng');
        return this.set('point', "POINT(" + lat + " " + lng + ")");
      }
    };

    Place.prototype.toJSON = function() {
      return {
        googlemapurl: this.get('googlemapurl'),
        point: this.get('point'),
        territoryno: this.get('territoryno'),
        routemarkernoafter: this.get('routemarkernoafter'),
        markerno: this.get('markerno'),
        blockno: this.get('blockno'),
        houseno: this.get('houseno'),
        description: this.get('description'),
        languages: this.get('languages'),
        persons: this.get('persons'),
        notes: this.get('notes'),
        interestlevel: this.get('interestlevel'),
        actions: this.get('actions')
      };
    };

    return Place;

  })(Backbone.Model);

  this.Boundaries = (function(_super) {

    __extends(Boundaries, _super);

    Boundaries.name = 'Boundaries';

    function Boundaries() {
      return Boundaries.__super__.constructor.apply(this, arguments);
    }

    Boundaries.prototype.model = Boundary;

    Boundaries.prototype.initialize = function(models, options) {
      this.queryParams = {};
      return this.resetUrl();
    };

    Boundaries.prototype.setQueryParam = function(name, value) {
      this.queryParams[name] = value;
      return this.resetUrl();
    };

    Boundaries.prototype.resetUrl = function() {
      var params;
      params = $.param(_.defaults(this.queryParams, DefaultParams));
      return this.url = "/api/v1/boundary/?" + params;
    };

    Boundaries.prototype.show = function() {
      var _this = this;
      this.trigger('show');
      return this.each(function(boundary) {
        return boundary.trigger('show');
      });
    };

    Boundaries.prototype.hide = function() {
      var _this = this;
      this.trigger('hide');
      return this.each(function(boundary) {
        return boundary.trigger('hide');
      });
    };

    return Boundaries;

  })(Backbone.Collection);

  this.Places = (function(_super) {

    __extends(Places, _super);

    Places.name = 'Places';

    function Places() {
      return Places.__super__.constructor.apply(this, arguments);
    }

    Places.prototype.model = Place;

    Places.prototype.comparator = function(place) {
      var routemarkernoafter;
      routemarkernoafter = place.get('routemarkernoafter');
      if (routemarkernoafter) {
        return routemarkernoafter + .5;
      } else {
        return place.get('markerno');
      }
    };

    Places.prototype.initialize = function(models, options) {
      this.queryParams = {};
      return this.resetUrl();
    };

    Places.prototype.setQueryParam = function(name, value) {
      this.queryParams[name] = value;
      return this.resetUrl();
    };

    Places.prototype.resetUrl = function() {
      var params;
      params = $.param(_.defaults(this.queryParams, DefaultParams));
      return this.url = "/api/v1/place/?" + params;
    };

    Places.prototype.show = function() {
      var _this = this;
      this.trigger('show');
      return this.each(function(place) {
        return place.trigger('show');
      });
    };

    Places.prototype.hide = function() {
      var _this = this;
      this.trigger('hide');
      return this.each(function(place) {
        return place.trigger('hide');
      });
    };

    return Places;

  })(Backbone.Collection);

  this.PlaceType = (function(_super) {

    __extends(PlaceType, _super);

    PlaceType.name = 'PlaceType';

    function PlaceType() {
      return PlaceType.__super__.constructor.apply(this, arguments);
    }

    PlaceType.prototype.idAttribute = 'id';

    PlaceType.prototype.initialize = function() {
      return this.places = new Places();
    };

    PlaceType.prototype.show = function() {
      this.trigger('show');
      return this.places.show();
    };

    PlaceType.prototype.hide = function() {
      this.trigger('hide');
      return this.places.hide();
    };

    return PlaceType;

  })(Backbone.Model);

  this.AppView = (function(_super) {

    __extends(AppView, _super);

    AppView.name = 'AppView';

    function AppView() {
      return AppView.__super__.constructor.apply(this, arguments);
    }

    AppView.prototype.initialize = function() {
      this.preferences = this.options.preferences;
      return this.render();
    };

    AppView.prototype.render = function() {
      var ll, pageheader, territoryno, zoom;
      this.mapView = new MapView({
        el: '#map',
        model: this.model,
        preferences: this.preferences
      }, territoryno = this.preferences.get('territoryno'), zoom = this.preferences.get('zoom'), (function() {
        switch (territoryno) {
          case "1-2-1":
            ll = "9.92111127977427,-84.1474170057183";
            zoom = 14;
            return pageheader = "1-2-1 San Jose/Escazu/Escazu/West";
          case "1-2-2":
            ll = "9.92111127977427,-84.1474170057183";
            zoom = 14;
            return pageheader = "1-2-2 San Jose/Escazu/Escazu/East";
          case "1-2-3 (A)":
            ll = "9.93246946647039,-84.1332120267754";
            zoom = 17;
            return pageheader = "1-2-3 (A) San Jose/Escazu/San Rafael/A";
          case "1-2-3 (B)":
            ll = "9.93162666503805,-84.1328338353043";
            zoom = 17;
            return pageheader = "1-2-3 (B) San Jose/Escazu/San Rafael/B";
          case "1-2-3 (3)":
            ll = "9.93138888367707,-84.1331557003861";
            zoom = 17;
            return pageheader = "1-2-3 (3) San Jose/Escazu/San Rafael/3";
          case "4-1-2":
            ll = "10.001025,-84.134588";
            pageheader = "4-1-2 Heredea/Heredia/Mercedes";
            return zoom = 17;
          case "4-7-1":
            ll = "9.98713594918928,-84.1771144239311";
            zoom = 15;
            return pageheader = "4-7-1 Heredea/Belen/La Ribera/La Ribera-San Antionio de Belen";
          case "4-7-3":
            ll = "9.970288,-84.156647";
            zoom = 17;
            return pageheader = "4-7-3 Heredea/Asuncion/Cariari/Ciudad Cariari";
          case "999":
            ll = "9.98713594918928,-84.1771144239311";
            zoom = 13;
            return pageheader = "999 Unassigned";
        }
      })(), $('.page-header').html(pageheader), territoryno ? (this.preferences.set('territoryno', territoryno), this.preferences.set('zoom', zoom)) : (this.preferences.set('zoom', 13), ll = "9.981192,-84.185314"), ll = ll.split(','), this.preferences.set('centerLat', ll[0]), this.preferences.set('centerLng', ll[1]));
      return this.searchView = new SearchView({
        el: '#search',
        model: this.model,
        preferences: this.preferences
      });
    };

    return AppView;

  })(Backbone.View);

  this.BoundariesView = (function(_super) {

    __extends(BoundariesView, _super);

    BoundariesView.name = 'BoundariesView';

    function BoundariesView() {
      this.addBoundaryItemView = __bind(this.addBoundaryItemView, this);

      this.render = __bind(this.render, this);
      return BoundariesView.__super__.constructor.apply(this, arguments);
    }

    BoundariesView.prototype.initialize = function() {
      var _this = this;
      this.map = this.options.map;
      this.preferences = this.options.preferences;
      this.territoryno = this.preferences.get('territoryno');
      this.boundaryItemViews = [];
      this.collection.bind('sync', function() {
        return _this.collection.fetch();
      });
      this.collection.bind('reset', this.render);
      if (this.collection.length > 0) return this.render();
    };

    BoundariesView.prototype.render = function() {
      var _this = this;
      _.each(this.boundaryItemViews, function(boundaryItemView) {
        return boundaryItemView.hide();
      });
      this.boundaryItemViews = [];
      this.collection.each(this.addBoundaryItemView);
      if (this.territoryno) return this.center();
    };

    BoundariesView.prototype.center = function() {
      var bounds, latlng, latlngs, terr, _i, _len;
      terr = this.collection.getByCid(territoryno);
      if (terr != null) {
        bounds = new google.maps.LatLngBounds();
        latlngs = terr.attributes.latlngs;
        for (_i = 0, _len = latlngs.length; _i < _len; _i++) {
          latlng = latlngs[_i];
          bounds.extend(latlng);
        }
        return this.map.setCenter(bounds.getCenter());
      }
    };

    BoundariesView.prototype.addBoundaryItemView = function(boundary) {
      var _this = this;
      boundary.bind('sync', function() {
        return _this.collection.fetch();
      });
      return this.boundaryItemViews.push(new BoundaryItemView({
        model: boundary,
        map: this.map
      }));
    };

    return BoundariesView;

  })(Backbone.View);

  this.BoundaryItemView = (function(_super) {

    __extends(BoundaryItemView, _super);

    BoundaryItemView.name = 'BoundaryItemView';

    function BoundaryItemView() {
      this.hide = __bind(this.hide, this);

      this.show = __bind(this.show, this);
      return BoundaryItemView.__super__.constructor.apply(this, arguments);
    }

    BoundaryItemView.prototype.roadmapPolyOpts = {
      strokeWeight: .5,
      strokeColor: '#000000',
      fillColor: '#000000',
      fillOpacity: 0.3
    };

    BoundaryItemView.prototype.hybridPolyOpts = {
      strokeWeight: .5,
      strokeColor: '#ffffff',
      fillColor: '#ffffff',
      fillOpacity: 0.3
    };

    BoundaryItemView.prototype.hoverPolyOpts = {
      strokeWeight: 2,
      fillColor: '#ffd700',
      fillOpacity: 0.01
    };

    BoundaryItemView.prototype.initialize = function() {
      this.map = this.options.map;
      this.model.bind('sync', this.show);
      return this.render();
    };

    BoundaryItemView.prototype.render = function() {
      var poly,
        _this = this;
      this.currentPolyOpts = this.roadmapPolyOpts;
      this.placeName = $('#placeName');
      poly = new google.maps.Polygon(this.currentPolyOpts);
      poly.setPath(this.model.get('latlngs'));
      poly.setMap(this.map);
      google.maps.event.addListener(poly, 'mouseover', function() {
        poly.setOptions(_this.hoverPolyOpts);
        _this.placeName.text(_this.model.get('id') + ' ' + _this.model.get('previousnumber') + ' ' + _this.model.get('name'));
        return _this.placeName.show();
      });
      google.maps.event.addListener(poly, 'mousemove', function() {
        _this.placeName.css('left', mouseX);
        return _this.placeName.css('top', mouseY);
      });
      google.maps.event.addListener(poly, 'mouseout', function() {
        poly.setOptions(_this.currentPolyOpts);
        return _this.placeName.hide();
      });
      return this.show();
    };

    BoundaryItemView.prototype.show = function() {};

    BoundaryItemView.prototype.hide = function() {};

    return BoundaryItemView;

  })(Backbone.View);

  this.MapView = (function(_super) {

    __extends(MapView, _super);

    MapView.name = 'MapView';

    function MapView() {
      this.onMapTypeChange = __bind(this.onMapTypeChange, this);
      return MapView.__super__.constructor.apply(this, arguments);
    }

    MapView.prototype.events = {
      'click button#add-place': '_addPlace'
    };

    MapView.prototype.initialize = function() {
      this.preferences = this.options.preferences;
      return this.render();
    };

    MapView.prototype.render = function() {
      var controlDiv, controlText, controlUI,
        _this = this;
      this.map = new google.maps.Map(this.$('#map-canvas').get(0), {
        zoom: this.preferences.get('zoom'),
        center: new google.maps.LatLng(this.preferences.get('centerLat'), this.preferences.get('centerLng')),
        mapTypeId: this.model.get('mapTypeId'),
        mapTypeControl: true,
        mapTypeControlOptions: {
          mapTypeIds: [google.maps.MapTypeId.ROADMAP, google.maps.MapTypeId.HYBRID]
        }
      });
      controlDiv = document.createElement('DIV');
      controlDiv.style.padding = '5px';
      controlUI = document.createElement('DIV');
      controlUI.style.backgroundColor = 'white';
      controlUI.style.borderStyle = 'solid';
      controlUI.style.borderWidth = '2px';
      controlUI.style.cursor = 'pointer';
      controlUI.style.textAlign = 'center';
      controlUI.title = 'Click to drop a new Place Marker';
      controlDiv.appendChild(controlUI);
      controlText = document.createElement('DIV');
      controlText.style.fontFamily = 'Arial,sans-serif';
      controlText.style.fontSize = '12px';
      controlText.style.paddingLeft = '4px';
      controlText.style.paddingRight = '4px';
      controlText.innerHTML = 'Add Place';
      controlUI.appendChild(controlText);
      google.maps.event.addListener(this.map, 'maptypeid_changed', this.onMapTypeChange);
      google.maps.event.addDomListener(controlUI, 'click', function() {
        return _this._addPlace();
      });
      this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv);
      google.maps.event.addListener(this.map, 'zoom_changed', function() {
        return _this.preferences.set('zoom', _this.map.getZoom());
      });
      this.userid = this.model.get('userid');
      if (this.userid > 0) {
        this.places = new Places();
        new PlacesView({
          collection: this.places,
          map: this.map
        });
        new ListView({
          collection: this.places
        });
        this.places.fetch();
        this.boundaries = new Boundaries();
        new BoundariesView({
          collection: this.boundaries,
          map: this.map,
          preferences: this.preferences
        });
        return this.boundaries.fetch();
      }
    };

    MapView.prototype._togglePlaceType = function(e) {
      var inputEl, model;
      inputEl = this.$(e.target);
      model = this.collection.get(inputEl.val());
      if (inputEl.is(":checked")) {
        return model.show();
      } else {
        return model.hide();
      }
    };

    MapView.prototype._addPlace = function() {
      var lat, lng;
      lat = this.map.getCenter().lat();
      lng = this.map.getCenter().lng();
      return this.places.create({
        territoryno: this.preferences.get('territoryno'),
        point: "POINT (" + lat + " " + lng + ")"
      });
    };

    MapView.prototype.onMapTypeChange = function() {
      switch (this.map.getMapTypeId()) {
        case google.maps.MapTypeId.ROADMAP:
        case google.maps.MapTypeId.HYBRID:
          return this.currentPolyOpts = this.roadmapPolyOpts;
        default:
          return this.currentPolyOpts = this.hybridPolyOpts;
      }
    };

    return MapView;

  })(Backbone.View);

  this.PlacesView = (function(_super) {

    __extends(PlacesView, _super);

    PlacesView.name = 'PlacesView';

    function PlacesView() {
      this.addPlaceItemView = __bind(this.addPlaceItemView, this);

      this.render = __bind(this.render, this);
      return PlacesView.__super__.constructor.apply(this, arguments);
    }

    PlacesView.prototype.initialize = function() {
      this.map = this.options.map;
      this.placeItemViews = [];
      this.collection.bind('add', this.addPlaceItemView);
      this.collection.bind('reset', this.render);
      if (this.collection.length > 0) return this.render();
    };

    PlacesView.prototype.render = function() {
      var _this = this;
      _.each(this.placeItemViews, function(placeItemView) {
        return placeItemView.hide();
      });
      this.placeItemViews = [];
      return this.collection.each(this.addPlaceItemView);
    };

    PlacesView.prototype.addPlaceItemView = function(place) {
      var _this = this;
      place.bind('sync', function() {
        return _this.collection.fetch();
      });
      return this.placeItemViews.push(new PlaceItemView({
        collection: this.collection,
        model: place,
        map: this.map
      }));
    };

    return PlacesView;

  })(Backbone.View);

  this.PlaceItemView = (function(_super) {

    __extends(PlaceItemView, _super);

    PlaceItemView.name = 'PlaceItemView';

    function PlaceItemView() {
      this.click = __bind(this.click, this);

      this.hide = __bind(this.hide, this);

      this.show = __bind(this.show, this);

      this.dragend = __bind(this.dragend, this);
      return PlaceItemView.__super__.constructor.apply(this, arguments);
    }

    PlaceItemView.prototype.initialize = function() {
      this.map = this.options.map;
      this.collection = this.options.collection;
      this.model.bind('show', this.show);
      this.model.bind('hide', this.hide);
      this.model.bind('sync', this.show);
      return this.render();
    };

    PlaceItemView.prototype.render = function() {
      this.marker = new google.maps.Marker({
        draggable: true
      });
      google.maps.event.addListener(this.marker, "dragend", this.dragend);
      google.maps.event.addListener(this.marker, "click", this.click);
      return this.show();
    };

    PlaceItemView.prototype.dragend = function() {
      if (confirm("Are you sure you want to move this marker?")) {
        this.model.set({
          lat: this.marker.position.lat(),
          lng: this.marker.position.lng()
        });
        this.model.save();
        return Log.log('dragged');
      } else {
        return this.marker.setPosition(new google.maps.LatLng(this.model.get('lat'), this.model.get('lng')));
      }
    };

    PlaceItemView.prototype.show = function() {
      var routemarkernoafter, title;
      this.position = new google.maps.LatLng(this.model.get('lat'), this.model.get('lng'));
      this.marker.setPosition(this.position);
      title = '';
      routemarkernoafter = this.model.get('routemarkernoafter');
      if (routemarkernoafter) title += ' Route AFTER #' + routemarkernoafter;
      title += ' ' + this.model.get('markerno');
      title += ' p' + this.model.get('id');
      if (this.model.get('interestlevel')) title += " INTERESTED! ";
      if (this.model.get('houseno') || this.model.get('description')) {
        title += "  ADDR: " + this.model.get('houseno');
        title += this.model.get('description');
      }
      if (this.model.get('persons')) {
        title += " " + "PERSONS: " + this.model.get('persons');
      }
      if (this.model.get('notes')) {
        title += " " + "NOTES: " + this.model.get('notes');
      }
      if (this.model.get('actions')) {
        title += " " + "ACTIONS: " + this.model.get('actions');
      }
      this.marker.setTitle(title);
      if (this.model.get('markerno')) {
        if (this.model.get('interestlevel')) {
          this.marker.setIcon('/static/img/mapicons/25x30/green/numbers/number_' + this.model.get('markerno') + '.png');
        } else {
          this.marker.setIcon('/static/img/mapicons/25x30/white/numbers/number_' + this.model.get('markerno') + '.png');
        }
      } else {
        this.marker.setIcon('/static/img/mapicons/25x30/white/symbol_blank.png');
      }
      return this.marker.setMap(this.map);
    };

    PlaceItemView.prototype.hide = function() {
      return this.marker.setMap(null);
    };

    PlaceItemView.prototype.click = function() {
      return this.infoWindow = new InfoWindow({
        collection: this.collection,
        model: this.model
      });
    };

    return PlaceItemView;

  })(Backbone.View);

  InfoWindow = (function(_super) {

    __extends(InfoWindow, _super);

    InfoWindow.name = 'InfoWindow';

    function InfoWindow() {
      return InfoWindow.__super__.constructor.apply(this, arguments);
    }

    InfoWindow.prototype.template = _.template($('#info-window-template').html());

    InfoWindow.prototype.editTemplate = _.template($('#edit-info-window-template').html());

    InfoWindow.prototype.className = 'modal';

    InfoWindow.prototype.events = {
      'click a.route': '_route',
      'click a.delete': '_delete',
      'click a.edit': '_edit',
      'click a.view': '_view',
      'click a.save-continue': '_saveContinue',
      'click a.save': '_save'
    };

    InfoWindow.prototype.initialize = function() {
      this.collection = this.options.collection;
      this.editing = this.options.editing || false;
      return this.render();
    };

    InfoWindow.prototype.render = function() {
      if (this.editing) {
        this.$el.html(this.editTemplate({
          model: this.model
        }));
      } else {
        this.$el.html(this.template({
          model: this.model
        }));
      }
      return this.$el.modal('show');
    };

    InfoWindow.prototype._edit = function() {
      this.editing = true;
      return this.render();
    };

    InfoWindow.prototype._route = function() {
      var params,
        _this = this;
      if (!confirm("Are you sure you want to route from this place?")) return;
      params = {};
      params = $.param(_.defaults(params, DefaultParams));
      $.get('/places/route/' + this.model.get('id') + '/?' + params, function(data) {
        return console.log(data);
      });
      this.collection.fetch();
      this.$el.modal('hide');
      return this.render();
    };

    InfoWindow.prototype._delete = function() {
      var _this = this;
      if (confirm("Are you sure you want to delete this place?")) {
        this.model.bind('destroy', function() {
          return _this.$el.modal('hide');
        });
        return this.model.destroy();
      }
    };

    InfoWindow.prototype._view = function() {
      if (confirm("Are you sure you want to abandon edit?")) {
        this.editing = false;
        return this.render();
      }
    };

    InfoWindow.prototype._saveContinue = function() {
      return this.persist();
    };

    InfoWindow.prototype._save = function() {
      var _this = this;
      this.persist();
      return this.model.bind('sync', function() {
        return _this.$el.modal('hide');
      });
    };

    InfoWindow.prototype.persist = function() {
      this.model.set({
        googlemapurl: this.$('#ed-googlemapurl').val(),
        territoryno: this.$('#ed-territoryno').val(),
        routemarkernoafter: Number(this.$('#ed-routemarkernoafter').val()),
        markerno: Number(this.$('#ed-markerno').val()),
        blockno: this.$('#ed-blockno').val(),
        interestlevel: Number(this.$('#ed-interestlevel').val()),
        houseno: this.$('#ed-houseno').val(),
        description: this.$('#ed-description').val(),
        languages: this.$('#ed-languages').val(),
        persons: this.$('#ed-persons').val(),
        notes: this.$('#ed-notes').val(),
        actions: this.$('#ed-actions').val()
      });
      return this.model.save();
    };

    return InfoWindow;

  })(Backbone.View);

  this.ListView = (function(_super) {

    __extends(ListView, _super);

    ListView.name = 'ListView';

    function ListView() {
      this.addListItemView = __bind(this.addListItemView, this);

      this.render = __bind(this.render, this);
      return ListView.__super__.constructor.apply(this, arguments);
    }

    ListView.prototype.initialize = function() {
      this.collection.bind('reset', this.render);
      this.collection.bind('add', this.addListItemView);
      if (this.collection.length > 0) return this.render();
    };

    ListView.prototype.render = function() {
      $('#list').empty();
      return this.collection.each(this.addListItemView);
    };

    ListView.prototype.addListItemView = function(model) {
      return new ListItemView({
        model: model
      });
    };

    return ListView;

  })(Backbone.View);

  this.ListItemView = (function(_super) {

    __extends(ListItemView, _super);

    ListItemView.name = 'ListItemView';

    function ListItemView() {
      return ListItemView.__super__.constructor.apply(this, arguments);
    }

    ListItemView.prototype.events = {
      'click .list-id': '_clickid'
    };

    ListItemView.prototype.initialize = function() {
      return this.render();
    };

    ListItemView.prototype.render = function() {
      var html;
      $('#list').append(this.el);
      html = '';
      html += '<div class="list-item-row" id="list-item-row-' + this.model.get('id') + '">';
      if (this.model.get('interestlevel')) {
        html += '<img src="/static/img/mapicons/25x30/green/numbers/number_' + this.model.get('markerno') + '.png" />';
      } else {
        html += '<img src="/static/img/mapicons/25x30/white/numbers/number_' + this.model.get('markerno') + '.png" />';
      }
      if (this.model.get('multiunit')) {
        html += '&nbsp;&nbsp;<span class="list-multiunit">MultiUnit</span>';
      }
      if (!this.model.get('residential')) {
        html += '&nbsp;&nbsp;<span class="list-residential">BIZ</span>';
      }
      if (!this.model.get('confirmed')) {
        html += '&nbsp;&nbsp;<span class="list-confirmed">?</span>';
      }
      html += '&nbsp;&nbsp;<span class="list-id">p' + this.model.get('id') + '</span>';
      if (this.model.get('interestlevel')) {
        html += '<span class="list-title list-interestlevel">INTEREST</span>';
      }
      if (this.model.get('houseno') || this.model.get('directions') || this.model.get('description')) {
        html += '<span class="list-title list-title">ADDRESS:</span>';
        if (this.model.get('houseno')) {
          html += '<span class="list-houseno">' + this.model.get('houseno') + '</span>&nbsp;';
        }
        if (this.model.get('directions')) {
          html += '<span class="list-directions">' + this.model.get('directions') + '</span>&nbsp;';
        }
        if (this.model.get('description')) {
          html += '<span class="list-description">' + this.model.get('description') + '</span>&nbsp;';
        }
      }
      if (this.model.get('persons')) {
        html += '<span class="list-title list-title">PERSON(S):</span>';
        html += '<span class="list-persons">' + this.model.get('persons') + '</span>';
      }
      if (this.model.get('notes')) {
        html += '<span class="list-title list-title">NOTES:</span>';
        html += '<span class="list-notes">' + this.model.get('notes') + '</span>';
      }
      if (this.model.get('actions')) {
        html += '<div class="list-item-actions" id="list-actions-' + this.model.get('id') + '">';
        html += '<span class="list-title list-title">ACTIONS:</span>';
        html += '<span class="list-actions">' + this.model.get('actions') + '</span>';
        html += '</div>';
      }
      html += '</div>';
      return this.$el.html(html);
    };

    ListItemView.prototype._clickid = function() {
      console.log('clickid');
      return this.infoWindow = new InfoWindow({
        model: this.model,
        editing: true
      });
    };

    return ListItemView;

  })(Backbone.View);

  this.LogView = (function(_super) {

    __extends(LogView, _super);

    LogView.name = 'LogView';

    function LogView() {
      return LogView.__super__.constructor.apply(this, arguments);
    }

    LogView.prototype.initialize = function() {
      Log.on('log', function(message) {
        return $('#log').append("<div>" + message + "</div>");
      });
      return this.render();
    };

    LogView.prototype.render = function() {};

    return LogView;

  })(Backbone.View);

  this.SearchView = (function(_super) {

    __extends(SearchView, _super);

    SearchView.name = 'SearchView';

    function SearchView() {
      return SearchView.__super__.constructor.apply(this, arguments);
    }

    return SearchView;

  })(Backbone.View);

  showBusy = function(x) {
    if (x) {
      return $('#busy').show();
    } else {
      return $('#busy').hide();
    }
  };

  showError = function(x) {
    if (x) {
      return $('#error').show();
    } else {
      return $('#error').hide();
    }
  };

  mouseX = null;

  mouseY = null;

  document.onmousemove = function(e) {
    mouseX = e.clientX;
    return mouseY = e.clientY;
  };

  CR = "10.001025 -84.134588";

  this.DefaultParams = {
    user_id: 0,
    username: "",
    api_key: "",
    format: "json",
    limit: 0
  };

  this.AppData = (function(_super) {

    __extends(AppData, _super);

    AppData.name = 'AppData';

    function AppData() {
      return AppData.__super__.constructor.apply(this, arguments);
    }

    AppData.prototype.defaults = {
      center: CR,
      zoom: 16,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    AppData.prototype.initialize = function(attributes) {
      var ll;
      ll = attributes.center.split(',');
      this.set('centerLat', ll[0]);
      this.set('centerLng', ll[1]);
      return $(document).ajaxError(function() {
        showBusy(false);
        return showError(true);
      });
    };

    return AppData;

  })(Backbone.Model);

  this.Preferences = (function() {

    Preferences.name = 'Preferences';

    function Preferences() {
      this.cookieName = "preferences";
      this.items = {};
      this.load();
    }

    Preferences.prototype.load = function() {
      var rawValue;
      rawValue = $.cookie(this.cookieName);
      if (rawValue) return this.items = JSON.parse(rawValue);
    };

    Preferences.prototype.save = function() {
      return $.cookie(this.cookieName, JSON.stringify(this.items), {
        expires: 365
      });
    };

    Preferences.prototype.get = function(key) {
      return this.items[key];
    };

    Preferences.prototype.set = function(key, value) {
      this.items[key] = value;
      return this.save();
    };

    Preferences.prototype.setDefault = function(key, defaultValue) {
      if (!this.items[key]) this.items[key] = defaultValue;
      return this.save();
    };

    return Preferences;

  })();

  this.Log = {
    log: function(message) {
      return this.trigger('log', message);
    }
  };

  _.extend(this.Log, Backbone.Events);

}).call(this);
