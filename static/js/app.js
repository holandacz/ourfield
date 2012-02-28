// Generated by CoffeeScript 1.2.1-pre
(function() {
  var EditInfoWindow,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  this.MapView = (function(_super) {

    __extends(MapView, _super);

    MapView.name = 'MapView';

    function MapView() {
      return MapView.__super__.constructor.apply(this, arguments);
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
      this.userid = this.model.get('userid');
      if (this.userid > 0) {
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

    PlaceTypeView.name = 'PlaceTypeView';

    function PlaceTypeView() {
      this.hide = __bind(this.hide, this);

      this.show = __bind(this.show, this);
      return PlaceTypeView.__super__.constructor.apply(this, arguments);
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
      this.model.bind('show', this.show);
      this.model.bind('hide', this.hide);
      this.model.bind('sync', this.show);
      return this.render();
    };

    PlaceItemView.prototype.render = function() {
      var title;
      this.position = new google.maps.LatLng(this.model.get('lat'), this.model.get('lng'));
      title = 'P' + this.model.get('id');
      if (this.model.get('interestlevel')) {
        title += " - INTEREST " + this.model.get('interestlevel');
      }
      if (this.model.get('territoryno')) {
        title += " - TERRITORY# " + this.model.get('territoryno');
      }
      if (this.model.get('sortno')) {
        title += " - SORT# " + this.model.get('sortno');
      }
      if (this.model.get('blockno')) {
        title += " - BLOCK# " + this.model.get('blockno');
      }
      if (this.model.get('houseno')) {
        title += " - HOUSE# " + this.model.get('houseno');
      }
      if (this.model.get('description')) {
        title += "\n\n" + "DESCRIPTION\n" + this.model.get('description');
      }
      if (this.model.get('persons')) {
        title += "\n\n" + "PERSONS\n" + this.model.get('persons');
      }
      if (this.model.get('actions')) {
        title += "\n\n" + "ACTIONS\n" + this.model.get('actions');
      }
      if (this.model.get('notes')) {
        title += "\n\n" + "NOTES\n" + this.model.get('notes');
      }
      this.marker = new google.maps.Marker({
        position: this.position,
        draggable: true,
        title: title
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
      if (confirm("Are you sure you want to move this marker?")) {
        this.model.set({
          lat: this.marker.position.lat(),
          lng: this.marker.position.lng()
        });
        return this.model.save();
      } else {
        this.marker.position = new google.maps.LatLng(this.model.get('lat'), this.model.get('lng'));
        return this.marker.setMap(this.map);
      }
    };

    PlaceItemView.prototype.show = function() {
      return this.marker.setMap(this.map);
    };

    PlaceItemView.prototype.hide = function() {
      return this.marker.setMap(null);
    };

    PlaceItemView.prototype.click = function() {
      return this.infoWindow.show();
    };

    return PlaceItemView;

  })(Backbone.View);

  this.InfoWindow = (function(_super) {

    __extends(InfoWindow, _super);

    InfoWindow.name = 'InfoWindow';

    function InfoWindow() {
      this.domReady = __bind(this.domReady, this);

      this.show = __bind(this.show, this);
      return InfoWindow.__super__.constructor.apply(this, arguments);
    }

    InfoWindow.prototype.template = _.template($('#info-window-template').html());

    InfoWindow.prototype.events = {
      'click button.edit': '_edit'
    };

    InfoWindow.prototype.initialize = function() {
      this.map = this.options.map;
      this.marker = this.options.marker;
      return this.render();
    };

    InfoWindow.prototype.render = function() {
      this.window = new google.maps.InfoWindow({
        maxWidth: 350
      });
      return google.maps.event.addListener(this.window, 'domready', this.domReady);
    };

    InfoWindow.prototype.show = function() {
      this.templateParams = {
        id: _.uniqueId('info-window-'),
        model: this.model
      };
      this.window.setContent(this.template(this.templateParams));
      return this.window.open(this.map, this.marker);
    };

    InfoWindow.prototype.hide = function() {
      return this.window.close();
    };

    InfoWindow.prototype.domReady = function() {
      return this.setElement($('#' + this.templateParams.id));
    };

    InfoWindow.prototype._edit = function() {
      return this.editInfoWindow = new EditInfoWindow({
        model: this.model
      });
    };

    return InfoWindow;

  })(Backbone.View);

  EditInfoWindow = (function(_super) {

    __extends(EditInfoWindow, _super);

    EditInfoWindow.name = 'EditInfoWindow';

    function EditInfoWindow() {
      return EditInfoWindow.__super__.constructor.apply(this, arguments);
    }

    EditInfoWindow.prototype.template = _.template($('#edit-info-window-template').html());

    EditInfoWindow.prototype.className = 'modal';

    EditInfoWindow.prototype.events = {
      'click a.save': '_save'
    };

    EditInfoWindow.prototype.initialize = function() {
      return this.render();
    };

    EditInfoWindow.prototype.render = function() {
      this.$el.html(this.template({
        model: this.model
      }));
      return this.$el.modal('show');
    };

    EditInfoWindow.prototype._save = function() {
      this.model.set({
        territoryno: this.$('#ed-territoryno').val(),
        sortno: this.$('#ed-sortno').val(),
        blockno: this.$('#ed-blockno').val(),
        interestlevel: this.$('#ed-interestlevel').val(),
        houseno: this.$('#ed-houseno').val(),
        description: this.$('#ed-description').val(),
        languages: this.$('#ed-languages').val(),
        persons: this.$('#ed-persons').val(),
        notes: this.$('#ed-notes').val(),
        actions: this.$('#ed-actions').val()
      });
      return this.model.save();
    };

    return EditInfoWindow;

  })(Backbone.View);

}).call(this);
