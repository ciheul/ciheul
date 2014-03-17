// socket.io
$(document).ready(function() {
  var socket = io.connect("http://localhost/jendela24/news");
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
