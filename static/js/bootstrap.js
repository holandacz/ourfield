// Generated by CoffeeScript 1.2.1-pre
(function() {

  $(function() {
    return App.addView("map", new MapView({
      el: $("#map"),
      bounds: App.bounds,
      ready: function() {
        return App.mapDidRender();
      }
    }));
  });

}).call(this);