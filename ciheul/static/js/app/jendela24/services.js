'use strict';

/* Services */

var ip_address = "localhost:8000";
//var ip_address = "192.168.1.100";

var jendela24Services = angular.module('jendela24Services', ['ngResource']);

jendela24Services.factory('News', ['$resource', 
  function($resource) {
    return $resource('http://' + ip_address + '/jendela24/1.0/news/?', {}, {
        query: {
          method: 'GET', 
          isArray: true,
          transformResponse: function(data_json, header) {
            var data = angular.fromJson(data_json);
            for (var i = 0; i < data.length; i++ ) {
              data[i].timeago = jQuery.timeago(data[i].published_at);
            }
            return data;
          }   
        }
    });
  }
]);


// socket.io
$(document).ready(function() {
  var server = 'http://' + ip_address + '/jendela24/news';
  var configuration = {
    'connect timeout': 5000, // 5 seconds
    'try multiple transports': true,
    'reconnect': true,
    'reconnection delay': 500,
    'reconnection limit': 5000,
    'max reconnection attempts': 3,
    'sync disconnect on unload': false,
    'flash policy port': 10843,
    'force new connection': true
  };
  var socket = io.connect(server, configuration);
  //var socket = io.connect("http://localhost/jendela24/news");
  // subscribe to server
  socket.emit("subscribe", {data: "hello"});
  
  // always listening if there is any update news
  socket.on("news_via_socketio", function(json_news) {
    // parse JSON
    var realtime_news = jQuery.parseJSON(json_news);
    
    // add the number of latest news to newsfeed
    var li = '<li><a href="">' + realtime_news.length + ' update news</a></li>';
    $(".realtime-newsfeed").append(li);

    // add the number of latest news to 'title' tag
    document.title = "(" + realtime_news.length + ") Jendela24";

    // attach event that when user clicks, it shows up all latest news
    // immediately
    $(".realtime-newsfeed li a").click(function(e) {
      for (var i = 0; i < realtime_news.length; i++) {
        var li = '<li>';
        li += '  <a href="' + realtime_news[i].url + '" target="_blank">';
        li += '    <div class="source">' + realtime_news[i].source + '</div>';
        li += '    <div class="title">' + realtime_news[i].title + '</div>';
        li += '    <div class="timeago"><time class="timeago" datetime="' + realtime_news[i].published_at + '">' + jQuery.timeago(realtime_news[i].published_at) + '</time></div>';
        li += '  </a></li>';
        $(".realtime-newsfeed").append(li);
      }
      // ensure appended news does not disappear
      e.preventDefault();

      // set the original title back
      document.title = "Jendela24";

      // remove the number of latest news from newsfeed
      $(".realtime-newsfeed li").first().remove();
    });
  });
});
