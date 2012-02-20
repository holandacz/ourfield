$ ->
  window.ulog = (msg) ->
    $("#log").append $("<div>" + msg + "</div>")

  Backbone.sync = (method, model, succeeded) ->
    ulog "<strong>" + method + ":</strong>  " + model.get("label")
    unless typeof model.cid is "undefined"
      cid = model.cid
      model.unset("cid").set
        id: cid
      ,
        silent: true
    succeeded model

  Model = Backbone.Model.extend()
  Models = Backbone.Collection.extend(model: Model)
  models = new Models([
    id: "m1"
    label: "Item 1"
  ,
    id: "m2"
    label: "Item 2"
   ])
  View = Backbone.View.extend(
    render: ->
      $(@el).html _.template("<input type=\"text\" value=\"<%= label %>\" />", @model.toJSON())
      this

    events:
      "change input": "change"

    change: ->
      newval = @$("input").val()
      ulog "<em>Changing " + @model.get("label") + " to " + newval + "</em>"
      @model.set label: newval
  )
  views = models.map((model) ->
    view = new View(model: model)
    $("#content").append view.render().el
    view
  )
  $("#save").click ->
    models.each (model) ->
      model.save()

  $("#add").click ->
    model = models.create(label: "New item")
    view = new View(model: model)
    $("#content").append view.render().el