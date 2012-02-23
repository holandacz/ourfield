(function() {
  var HomeController,
    __hasProp = Object.prototype.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  HomeController = (function(_super) {

    __extends(HomeController, _super);

    function HomeController() {
      HomeController.__super__.constructor.apply(this, arguments);
    }

    HomeController.prototype.routes = {
      "markers/marker/:action/:id": "sendActionToMarker"
    };

    return HomeController;

  })(Backbone.Router);

  window.HomeController = HomeController;

}).call(this);
