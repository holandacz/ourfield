(->
  
  window.Tweet = Backbone.Model.extend(urlRoot: TWEET_API)
  window.Tweets = Backbone.Collection.extend(
    urlRoot: TWEET_API
    model: Tweet
    maybeFetch: (options) ->
      if @_fetched
        options.success and options.success()
        return
      self = this
      successWrapper = (success) ->
        ->
          self._fetched = true
          success and success.apply(this, arguments)

      options.success = successWrapper(options.success)
      @fetch options

    getOrFetch: (id, options) ->
      model = @get(id)
      if model
        options.success and options.success(model)
        return
      model = new Tweet(resource_uri: id)
      model.fetch options
  )
  window.TweetView = Backbone.View.extend(
    tagName: "li"
    className: "tweet"
    events:
      "click .permalink": "navigate"

    initialize: ->
      @model.bind "change", @render, this

    navigate: (e) ->
      @trigger "navigate", @model
      e.preventDefault()

    render: ->
      $(@el).html ich.tweetTemplate(@model.toJSON())
      this
  )
  window.DetailApp = Backbone.View.extend(
    events:
      "click .home": "home"

    home: (e) ->
      @trigger "home"
      e.preventDefault()

    render: ->
      $(@el).html ich.detailApp(@model.toJSON())
      this
  )
  window.InputView = Backbone.View.extend(
    events:
      "click .tweet": "createTweet"
      "keypress #message": "createOnEnter"

    createOnEnter: (e) ->
      if (e.keyCode or e.which) is 13
        @createTweet()
        e.preventDefault()

    createTweet: ->
      message = @$("#message").val()
      if message
        @collection.create message: message
        @$("#message").val ""
  )
  window.ListView = Backbone.View.extend(
    initialize: ->
      _.bindAll this, "addOne", "addAll"
      @collection.bind "add", @addOne
      @collection.bind "reset", @addAll, this
      @views = []

    addAll: ->
      @views = []
      @collection.each @addOne

    addOne: (tweet) ->
      view = new TweetView(model: tweet)
      $(@el).prepend view.render().el
      @views.push view
      view.bind "all", @rethrow, this

    rethrow: ->
      @trigger.apply this, arguments
  )
  window.ListApp = Backbone.View.extend(
    el: "#app"
    rethrow: ->
      @trigger.apply this, arguments

    render: ->
      $(@el).html ich.listApp({})
      list = new ListView(
        collection: @collection
        el: @$("#tweets")
      )
      list.addAll()
      list.bind "all", @rethrow, this
      new InputView(
        collection: @collection
        el: @$("#input")
      )
  )
  window.Router = Backbone.Router.extend(
    routes:
      "": "list"
      ":id/": "detail"

    navigate_to: (model) ->
      path = (model and model.get("id") + "/") or ""
      @navigate path, true

    detail: ->

    list: ->
  )
  $ ->
    window.app = window.app or {}
    app.router = new Router()
    app.tweets = new Tweets()
    app.list = new ListApp(
      el: $("#app")
      collection: app.tweets
    )
    app.detail = new DetailApp(el: $("#app"))
    app.router.bind "route:list", ->
      app.tweets.maybeFetch success: _.bind(app.list.render, app.list)

    app.router.bind "route:detail", (id) ->
      app.tweets.getOrFetch app.tweets.urlRoot + id + "/",
        success: (model) ->
          app.detail.model = model
          app.detail.render()

    app.list.bind "navigate", app.router.navigate_to, app.router
    app.detail.bind "home", app.router.navigate_to, app.router
    Backbone.history.start
      pushState: true
      silent: app.loaded
)()