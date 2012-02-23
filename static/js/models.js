(function() {
  var CR,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; },
    __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  CR = "10.001025 -84.134588";

  this.DefaultParams = {
    username: "larry",
    api_key: "d65af2857fc77e4ce56299e53f6858178dfab295",
    format: "json",
    limit: 5
  };

  this.AppData = (function(_super) {

    __extends(AppData, _super);

    function AppData() {
      AppData.__super__.constructor.apply(this, arguments);
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

  this.Place = (function(_super) {

    __extends(Place, _super);

    function Place() {
      this.recalcPoint = __bind(this.recalcPoint, this);
      Place.__super__.constructor.apply(this, arguments);
    }

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
      lat = this.get('lat');
      lng = this.get('lng');
      return this.set('point', "POINT(" + lat + " " + lng + ")");
    };

    Place.prototype.toJSON = function() {
      return {
        point: this.get('point')
      };
    };

    return Place;

  })(Backbone.Model);

  this.Places = (function(_super) {

    __extends(Places, _super);

    function Places() {
      Places.__super__.constructor.apply(this, arguments);
    }

    Places.prototype.model = Place;

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

    function PlaceType() {
      PlaceType.__super__.constructor.apply(this, arguments);
    }

    PlaceType.prototype.idAttribute = 'id';

    PlaceType.prototype.initialize = function() {
      var params;
      this.places = new Places();
      params = {};
      params = $.param(_.defaults(params, DefaultParams));
      return this.places.url = "/api/v1/place/?" + params;
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

    function PlaceTypes() {
      PlaceTypes.__super__.constructor.apply(this, arguments);
    }

    PlaceTypes.prototype.model = PlaceType;

    return PlaceTypes;

  })(Backbone.Collection);

}).call(this);
