class HomeController extends Backbone.Router
  routes:
    "markers/marker/:action/:id": "sendActionToMarker"

window.HomeController = HomeController