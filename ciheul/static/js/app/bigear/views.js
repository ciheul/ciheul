var app = app || {};

app.ReportView = Backbone.View.extend({
  tagName: 'div',
  className: 'reportContainer',
  template: _.template($('#report-template').html()),

  render: function() {
    // convert ISO8601 to time since format
    if (typeof(this.model.get('created_at')) === 'undefined') {
      this.model.set('created_at', jQuery.timeago(new Date()));
    }
    else {
      this.model.set('created_at', jQuery.timeago(this.model.get('created_at')));
    }
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

  events: {
    'click #add': 'addReport'
  },

  addReport: function(e) {
    e.preventDefault();

    var formData = {};
    $('#addReport div').children('input').each(function(i, el) {
      if ($(el).val() !== '') {
        formData[el.id] = $(el).val();
      }
    });

    this.collection.create(formData);
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