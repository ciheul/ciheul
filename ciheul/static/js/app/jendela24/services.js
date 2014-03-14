// socket.io
$(document).ready(function() {
  var socket = io.connect("http://192.168.1.102/jendela24/news");
  socket.emit("subscribe", {data: "hello"});
  socket.on("news_via_socketio", function(data) {
    $(".news_title").append(data);
  });
});
