var app = app || {};

app.Report = Backbone.Model.extend({
  defaults: {},        
});


app.Timeline = Backbone.Collection.extend({
  url: '/report',
  model: app.Report,
});
