(function() {

  (function() {
    window.Tweet = Backbone.Model.extend({
      urlRoot: TWEET_API
    });
    window.Tweets = Backbone.Collection.extend({
      urlRoot: TWEET_API,
      model: Tweet,
      maybeFetch: function(options) {
        var self, successWrapper;
        if (this._fetched) {
          options.success && options.success();
          return;
        }
        self = this;
        successWrapper = function(success) {
          return function() {
            self._fetched = true;
            return success && success.apply(this, arguments);
          };
        };
        options.success = successWrapper(options.success);
        return this.fetch(options);
      },
      getOrFetch: function(id, options) {
        var model;
        model = this.get(id);
        if (model) {
          options.success && options.success(model);
          return;
        }
        model = new Tweet({
          resource_uri: id
        });
        return model.fetch(options);
      }
    });
    window.TweetView = Backbone.View.extend({
      tagName: "li",
      className: "tweet",
      events: {
        "click .permalink": "navigate"
      },
      initialize: function() {
        return this.model.bind("change", this.render, this);
      },
      navigate: function(e) {
        this.trigger("navigate", this.model);
        return e.preventDefault();
      },
      render: function() {
        $(this.el).html(ich.tweetTemplate(this.model.toJSON()));
        return this;
      }
    });
    window.DetailApp = Backbone.View.extend({
      events: {
        "click .home": "home"
      },
      home: function(e) {
        this.trigger("home");
        return e.preventDefault();
      },
      render: function() {
        $(this.el).html(ich.detailApp(this.model.toJSON()));
        return this;
      }
    });
    window.InputView = Backbone.View.extend({
      events: {
        "click .tweet": "createTweet",
        "keypress #message": "createOnEnter"
      },
      createOnEnter: function(e) {
        if ((e.keyCode || e.which) === 13) {
          this.createTweet();
          return e.preventDefault();
        }
      },
      createTweet: function() {
        var message;
        message = this.$("#message").val();
        if (message) {
          this.collection.create({
            message: message
          });
          return this.$("#message").val("");
        }
      }
    });
    window.ListView = Backbone.View.extend({
      initialize: function() {
        _.bindAll(this, "addOne", "addAll");
        this.collection.bind("add", this.addOne);
        this.collection.bind("reset", this.addAll, this);
        return this.views = [];
      },
      addAll: function() {
        this.views = [];
        return this.collection.each(this.addOne);
      },
      addOne: function(tweet) {
        var view;
        view = new TweetView({
          model: tweet
        });
        $(this.el).prepend(view.render().el);
        this.views.push(view);
        return view.bind("all", this.rethrow, this);
      },
      rethrow: function() {
        return this.trigger.apply(this, arguments);
      }
    });
    window.ListApp = Backbone.View.extend({
      el: "#app",
      rethrow: function() {
        return this.trigger.apply(this, arguments);
      },
      render: function() {
        var list;
        $(this.el).html(ich.listApp({}));
        list = new ListView({
          collection: this.collection,
          el: this.$("#tweets")
        });
        list.addAll();
        list.bind("all", this.rethrow, this);
        return new InputView({
          collection: this.collection,
          el: this.$("#input")
        });
      }
    });
    window.Router = Backbone.Router.extend({
      routes: {
        "": "list",
        ":id/": "detail"
      },
      navigate_to: function(model) {
        var path;
        path = (model && model.get("id") + "/") || "";
        return this.navigate(path, true);
      },
      detail: function() {},
      list: function() {}
    });
    return $(function() {
      window.app = window.app || {};
      app.router = new Router();
      app.tweets = new Tweets();
      app.list = new ListApp({
        el: $("#app"),
        collection: app.tweets
      });
      app.detail = new DetailApp({
        el: $("#app")
      });
      app.router.bind("route:list", function() {
        return app.tweets.maybeFetch({
          success: _.bind(app.list.render, app.list)
        });
      });
      app.router.bind("route:detail", function(id) {
        return app.tweets.getOrFetch(app.tweets.urlRoot + id + "/", {
          success: function(model) {
            app.detail.model = model;
            return app.detail.render();
          }
        });
      });
      app.list.bind("navigate", app.router.navigate_to, app.router);
      app.detail.bind("home", app.router.navigate_to, app.router);
      return Backbone.history.start({
        pushState: true,
        silent: app.loaded
      });
    });
  })();

}).call(this);
