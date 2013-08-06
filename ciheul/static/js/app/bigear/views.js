var app = app || {};

app.ReportView = Backbone.View.extend({
  tagName: 'div',
  className: 'reportContainer',
  template: _.template($('#report-template').html()),

  render: function() {
    this.$el.html(this.template(this.model.toJSON()));
    return this;
  },
});


app.TimelineView = Backbone.View.extend({
  el: '.timeline',

  initialize: function() {
    this.collection = new app.Timeline();
    this.collection.fetch({reset: true});
    this.render();

    this.listenTo(this.collection, 'add', this.renderReport);
    this.listenTo(this.collection, 'reset', this.render);
  },

  render: function() {
    this.collection.each(function(item) {
      this.renderReport(item);
    }, this);
  },

  renderReport: function(item) {
    var reportView = new app.ReportView({
      model: item
    });              
    this.$el.append(reportView.render().el);
  },
});
