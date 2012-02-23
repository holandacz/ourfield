(function() {
  var __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  this.MapView = (function(_super) {

    __extends(MapView, _super);

    function MapView() {
      MapView.__super__.constructor.apply(this, arguments);
    }

    MapView.prototype.events = {
      'click input[type="checkbox"]': '_togglePlaceType',
      'click button#add-place': '_addPlace'
    };

    MapView.prototype.initialize = function() {
      return this.render();
    };

    MapView.prototype.render = function() {
      var _this = this;
      this.map = new google.maps.Map(this.$('#map-canvas').get(0), {
        zoom: this.model.get('zoom'),
        center: new google.maps.LatLng(this.model.get('centerLat'), this.model.get('centerLng')),
        mapTypeId: this.model.get('mapTypeId')
      });
      this.collection.each(function(placeType) {
        return new PlaceTypeView({
          model: placeType,
          collection: placeType.places,
          map: _this.map
        });
      });
      return this.$('input[type="checkbox"]:checked').each(function(index, el) {
        var model;
        model = _this.collection.get($(el).val());
        return model.show();
      });
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

    MapView.prototype._addPlace = function(e) {
      var lat, lng;
      console.log("_addPlace", e);
      lat = this.map.getCenter().lat();
      lng = this.map.getCenter().lng();
      return this.collection.get(1).places.create({
        point: "POINT (" + lat + " " + lng + ")"
      });
    };

    return MapView;

  })(Backbone.View);

  this.PlaceTypeView = (function(_super) {

    __extends(PlaceTypeView, _super);

    function PlaceTypeView() {
      this.hide = __bind(this.hide, this);
      this.show = __bind(this.show, this);
      PlaceTypeView.__super__.constructor.apply(this, arguments);
    }

    PlaceTypeView.prototype.initialize = function() {
      this.map = this.options.map;
      this.model.bind('show', this.show);
      this.model.bind('hide', this.hide);
      return this.render();
    };

    PlaceTypeView.prototype.render = function() {
      return this.placesView = new PlacesView({
        collection: this.collection,
        map: this.map
      });
    };

    PlaceTypeView.prototype.show = function() {
      return this.collection.fetch();
    };

    PlaceTypeView.prototype.hide = function() {};

    return PlaceTypeView;

  })(Backbone.View);

  this.PlacesView = (function(_super) {

    __extends(PlacesView, _super);

    function PlacesView() {
      this.addPlaceItemView = __bind(this.addPlaceItemView, this);
      this.render = __bind(this.render, this);
      PlacesView.__super__.constructor.apply(this, arguments);
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
      return this.collection.each(this.addPlaceItemView);
    };

    PlacesView.prototype.addPlaceItemView = function(place) {
      return this.placeItemViews.push(new PlaceItemView({
        model: place,
        map: this.map
      }));
    };

    return PlacesView;

  })(Backbone.View);

  this.PlaceItemView = (function(_super) {

    __extends(PlaceItemView, _super);

    function PlaceItemView() {
      this.click = __bind(this.click, this);
      this.persist = __bind(this.persist, this);
      this.hide = __bind(this.hide, this);
      this.show = __bind(this.show, this);
      this.dragend = __bind(this.dragend, this);
      PlaceItemView.__super__.constructor.apply(this, arguments);
    }

    PlaceItemView.prototype.initialize = function() {
      this.map = this.options.map;
      this.model.bind('show', this.show);
      this.model.bind('hide', this.hide);
      this.model.bind('change', this.persist);
      return this.render();
    };

    PlaceItemView.prototype.render = function() {
      this.position = new google.maps.LatLng(this.model.get('lat'), this.model.get('lng'));
      this.marker = new google.maps.Marker({
        position: this.position,
        draggable: true,
        animation: google.maps.Animation.DROP,
        title: this.position.lat() + "," + this.position.lng()
      });
      this.infoWindow = new InfoWindow({
        map: this.map,
        marker: this.marker,
        model: this.model
      });
      google.maps.event.addListener(this.marker, "dragend", this.dragend);
      google.maps.event.addListener(this.marker, "click", this.click);
      return this.show();
    };

    PlaceItemView.prototype.dragend = function() {
      console.log('PlaceItemView#dragend');
      return this.model.set({
        lat: this.marker.position.Qa,
        lng: this.marker.position.Ra
      });
    };

    PlaceItemView.prototype.show = function() {
      return this.marker.setMap(this.map);
    };

    PlaceItemView.prototype.hide = function() {
      return this.marker.setMap(null);
    };

    PlaceItemView.prototype.persist = function() {
      return this.model.save();
    };

    PlaceItemView.prototype.click = function() {
      console.log("PlaceItemView#click");
      return this.infoWindow.show();
    };

    return PlaceItemView;

  })(Backbone.View);

  this.InfoWindow = (function(_super) {

    __extends(InfoWindow, _super);

    function InfoWindow() {
      this.domReady = __bind(this.domReady, this);
      InfoWindow.__super__.constructor.apply(this, arguments);
    }

    InfoWindow.prototype.template = _.template($('#info-window-template').html());

    InfoWindow.prototype.events = {
      'click button.edit': '_edit'
    };

    InfoWindow.prototype.initialize = function() {
      this.map = this.options.map;
      this.marker = this.options.marker;
      this.htmlId = _.uniqueId('info-window-');
      return this.render();
    };

    InfoWindow.prototype.render = function() {
      this.window = new google.maps.InfoWindow({
        maxWidth: 200
      });
      return google.maps.event.addListener(this.window, 'domready', this.domReady);
    };

    InfoWindow.prototype.show = function() {
      this.window.setContent(this.template({
        model: this.model,
        html_id: this.htmlId
      }));
      return this.window.open(this.map, this.marker);
    };

    InfoWindow.prototype.hide = function() {
      return this.window.close();
    };

    InfoWindow.prototype.domReady = function() {
      return this.setElement($('#' + this.htmlId));
    };

    InfoWindow.prototype._edit = function() {
      return console.log("I am editing now!");
    };

    return InfoWindow;

  })(Backbone.View);

}).call(this);