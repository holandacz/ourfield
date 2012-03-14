// Generated by CoffeeScript 1.2.1-pre
(function() {
  var CR, InfoWindow,
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; },
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

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

  this.Places = (function(_super) {

    __extends(Places, _super);

    Places.name = 'Places';

    function Places() {
      return Places.__super__.constructor.apply(this, arguments);
    }

    Places.prototype.model = Place;

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

  this.PlaceTypes = (function(_super) {

    __extends(PlaceTypes, _super);

    PlaceTypes.name = 'PlaceTypes';

    function PlaceTypes() {
      return PlaceTypes.__super__.constructor.apply(this, arguments);
    }

    PlaceTypes.prototype.model = PlaceType;

    return PlaceTypes;

  })(Backbone.Collection);

  this.AppView = (function(_super) {

    __extends(AppView, _super);

    AppView.name = 'AppView';

    function AppView() {
      return AppView.__super__.constructor.apply(this, arguments);
    }

    AppView.prototype.initialize = function() {
      var _this = this;
      this.preferences = this.options.preferences;
      this.collection.bind('sync', function() {
        return _this.collection.fetch();
      });
      return this.render();
    };

    AppView.prototype.render = function() {
      var ll, pageheader, territoryno, zoom;
      this.mapView = new MapView({
        el: '#map',
        model: this.model,
        collection: this.collection,
        preferences: this.preferences
      }, territoryno = this.preferences.get('territoryno'), zoom = this.preferences.get('zoom'), console.log(territoryno), (function() {
        switch (territoryno) {
          case "1-2-1":
            ll = "9.92111127977427,-84.1474170057183";
            zoom = 14;
            return pageheader = "San Jose/Escazu/Escazu/West";
          case "1-2-2":
            ll = "9.92111127977427,-84.1474170057183";
            zoom = 14;
            return pageheader = "San Jose/Escazu/Escazu/East";
          case "4-1-2":
            ll = "10.001025,-84.134588";
            pageheader = "Heredea/Heredia/Mercedes";
            return zoom = 15;
          case "4-7-1":
            ll = "9.98713594918928,-84.1771144239311";
            zoom = 15;
            return pageheader = "Heredea/Belen/La Ribera/La Ribera-San Antionio de Belen";
          case "999":
            ll = "9.98713594918928,-84.1771144239311";
            zoom = 13;
            return pageheader = "Unassigned";
        }
      })(), $('#page-header').html(pageheader), territoryno ? (this.preferences.set('territoryno', territoryno), this.preferences.set('center', ll), this.preferences.set('zoom', zoom), ll = ll.split(','), this.preferences.set('centerLat', ll[0]), this.preferences.set('centerLng', ll[1])) : void 0);
      this.listView = new ListView({
        el: '#list',
        model: this.model,
        collection: this.collection.get(1).places,
        preferences: this.preferences
      });
      return this.searchView = new SearchView({
        el: '#search',
        model: this.model,
        collection: this.collection,
        preferences: this.preferences
      });
    };

    return AppView;

  })(Backbone.View);

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
      this.preferences = this.options.preferences;
      return this.render();
    };

    MapView.prototype.render = function() {
      var controlDiv, controlText, controlUI,
        _this = this;
      this.map = new google.maps.Map(this.$('#map-canvas').get(0), {
        zoom: this.preferences.get('zoom'),
        center: new google.maps.LatLng(this.preferences.get('centerLat'), this.preferences.get('centerLng')),
        mapTypeId: this.model.get('mapTypeId')
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
      google.maps.event.addDomListener(controlUI, 'click', function() {
        return _this._addPlace();
      });
      this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(controlDiv);
      google.maps.event.addListener(this.map, 'zoom_changed', function() {
        return _this.preferences.set('zoom', _this.map.getZoom());
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

    MapView.prototype._addPlace = function() {
      var lat, lng;
      lat = this.map.getCenter().lat();
      lng = this.map.getCenter().lng();
      console.log('preferences', this.preferences.items);
      return this.collection.get(1).places.create({
        territoryno: this.preferences.get('territoryno'),
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
      this.placeItemViews = [];
      return this.collection.each(this.addPlaceItemView);
    };

    PlacesView.prototype.addPlaceItemView = function(place) {
      var _this = this;
      place.bind('sync', function() {
        return _this.collection.fetch();
      });
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
      var title;
      this.position = new google.maps.LatLng(this.model.get('lat'), this.model.get('lng'));
      this.marker.setPosition(this.position);
      title = this.model.get('markerno');
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
        this.marker.setIcon('/static/img/mapicons/25x30/numbers/number_' + this.model.get('markerno') + '.png');
      } else {
        this.marker.setIcon('/static/img/mapicons/25x30/symbol_blank.png');
      }
      return this.marker.setMap(this.map);
    };

    PlaceItemView.prototype.hide = function() {
      return this.marker.setMap(null);
    };

    PlaceItemView.prototype.click = function() {
      return this.infoWindow = new InfoWindow({
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
      'click a.delete': '_delete',
      'click a.edit': '_edit',
      'click a.view': '_view',
      'click a.save-continue': '_saveContinue',
      'click a.save': '_save'
    };

    InfoWindow.prototype.initialize = function() {
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
      html += '<img src="/static/img/mapicons/25x30/numbers/number_' + this.model.get('markerno') + '.png" />';
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

    SearchView.prototype.initilaize = function() {
      return this.render();
    };

    SearchView.prototype.render = function() {};

    return SearchView;

  })(Backbone.View);

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
      return this.set('centerLng', ll[1]);
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
