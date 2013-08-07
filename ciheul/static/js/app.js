var app = app || {};


$(function() {
  new app.TimelineView();

  
  function showPosition(position) {
    x.innerHTML = "<p>(" + position.coords.longitude + ", " + position.coords.latitude + ")";
  }

  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition);
    } 
  }

  var x = document.getElementById('geolocation');
  getLocation(showPosition);


});
