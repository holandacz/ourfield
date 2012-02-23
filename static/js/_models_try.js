(function() {
  var View, views;

  $(function() {
    var Model, Models, models;
    window.ulog = function(msg) {
      return $("#log").append($("<div>" + msg + "</div>"));
    };
    Backbone.sync = function(method, model, succeeded) {
      var cid;
      ulog("<strong>" + method + ":</strong>  " + model.get("label"));
      if (typeof model.cid !== "undefined") {
        cid = model.cid;
        model.unset("cid").set({
          id: cid
        }, {
          silent: true
        });
      }
      return succeeded(model);
    };
    Model = Backbone.Model.extend();
    Models = Backbone.Collection.extend({
      model: Model
    });
    return models = new Models([
      {
        id: "m1",
        label: "Item 1"
      }, {
        id: "m2",
        label: "Item 2"
      }
    ]);
  });

  View = Backbone.View.extend({
    render: function() {
      $(this.el).html(_.template("<input type=\"text\" value=\"<%= label %>\" />", this.model.toJSON()));
      return this;
    },
    events: {
      "change input": "change"
    },
    change: function() {
      var newval;
      newval = this.$("input").val();
      ulog("<em>Changing " + this.model.get("label") + " to " + newval + "</em>");
      return this.model.set({
        label: newval
      });
    }
  });

  views = models.map(function(model) {
    var view;
    view = new View({
      model: model
    });
    $("#content").append(view.render().el);
    return view;
  });

  $("#save").click(function() {
    return models.each(function(model) {
      return model.save();
    });
  });

  $("#add").click(function() {
    var model, view;
    model = models.create({
      label: "New item"
    });
    view = new View({
      model: model
    });
    return $("#content").append(view.render().el);
  });

}).call(this);
