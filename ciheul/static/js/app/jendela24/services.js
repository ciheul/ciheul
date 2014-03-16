// socket.io
$(document).ready(function() {
  var socket = io.connect("http://192.168.1.100/jendela24/news");
  socket.emit("subscribe", {data: "hello"});
  socket.on("news_via_socketio", function(title, source, published_at) {
    console.log(source + " " + title);
    var li = "<li>" + source + " " + title + " " + jQuery.timeago(published_at) + "</li>";
    console.log(li);
    $(".realtime-newsfeed").append(li);
  });
});
