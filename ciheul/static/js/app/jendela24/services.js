// socket.io
$(document).ready(function() {
  var socket = io.connect("http://localhost/jendela24/news");
  socket.emit("subscribe", {data: "hello"});
  socket.on("news_via_socketio", function(json_news) {
    console.log(json_news); 
    var realtime_news = jQuery.parseJSON(json_news);
    console.log(realtime_news.length);
    var li = '<li>';
    li += '  <a href="#">' + realtime_news.length + " update news";
    li += '  </a></li>';
    $(".realtime-newsfeed").append(li);
    $(".realtime-newsfeed").addEventListener('click', function() {
      for (var i = 0; i < realtime_news.length; i++) {
        var li = '<li>';
        li += '  <a href="' + realtime_news[i].url + '" target="_blank">';
        li += '    <div class="source">' + realtime_news[i].source + '</div>';
        li += '    <div class="title">' + realtime_news[i].title + '</div>';
        li += '    <div class="timeago"><time class="timeago" datetime="' + realtime_news[i].published_at + '">' + jQuery.timeago(realtime_news[i].published_at) + '</time></div>';
        li += '  </a></li>';
        $(".realtime-newsfeed").append(li);
      }
    }, false);
  });

  //socket.on("news_via_socketio", function(title, source, published_at, url) {
  //  var li = '<li>';
  //  li += '  <a href="' + url + '" target="_blank">';
  //  li += '    <div class="source">' + source + '</div>';
  //  li += '    <div class="title">' + title + '</div>';
  //  li += '    <div class="timeago"><time class="timeago" datetime="' + published_at + '">' + jQuery.timeago(published_at) + '</time></div>';
  //  li += '  </a></li>';
  //  $(".realtime-newsfeed").append(li);
  //});
});
