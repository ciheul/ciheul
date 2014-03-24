'use strict';

/* Controllers */

var jendela24Controllers = angular.module('jendela24Controllers', ['ui.bootstrap']);

jendela24Controllers.controller('NewsFeedCtrl', ['$scope', 'News',
  function($scope, News) {
    var limit = 40;
    $scope.newsfeed = News.query({offset: 0, limit: limit});

    var counter = limit;
    $(window).scroll(function() {
      if ($(window).scrollTop() + $(window).height() > $(document).height() - 10) {
        console.log("bottom!");
        if ($(".spinning").children().length === 0) {
          console.log("spinning!");
          var img = '<img src="/static/img/common/spin-white.gif">';
          $(".spinning").append(img);

          News.query({offset: counter, limit: limit}, 
            function success(result) {
              console.log(counter);
              //$scope.newsfeed.push($scope.newsfeed, result);
              for (var i = 0; i < result.length; i++) {      
                console.log(result[i]);
                var li = '<li>';
                li += '  <a href="' + result[i].url + '" target="_blank">';
                li += '    <div class="source">' + result[i].source + '</div>';
                li += '    <div class="title">' + result[i].title + '</div>';
                li += '    <div class="timeago"><time class="timeago" datetime="' + result[i].published_at + '">' + jQuery.timeago(result[i].published_at) + '</time></div>';
                li += '  </a></li>';
                $(".newsfeed").append(li);
              }
              $(".spinning").remove();
            }
          );
          counter += limit;
        }
      }
    });
  }]
);

jendela24Controllers.controller('ModalDemoCtrl', ['$scope', '$modal', '$log',
  function($scope, $modal, $log) {
    $scope.items = ['item1', 'item2', 'item3'];

    $scope.open = function() {
      var modalInstance = $modal.open({
        templateUrl: '/static/partials/jendela24/login_modal.html',
        controller: ModalInstanceCtrl,
        resolve: {
          items: function() {
            return $scope.items;
          }
        }
      });

      modalInstance.result.then(function(selectedItem) {
        $scope.selected = $scope.selectedItem;
      }, function () {
        $log.info('Modal dismissed at: ' + new Date());
      });
    };
  }]
);

var ModalInstanceCtrl = function($scope, $modalInstance, items) {
  $scope.items = items;
  
  $scope.selected = {
    item: $scope.items[0]
  };

  $scope.ok = function() {
    $modalInstance.close($scope.selected.item);
  };

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
};


          //$(".realtime-newsfeed li a").click(function(e) {
          //  for (var i = 0; i < realtime_news.length; i++) {
          //    var li = '<li>';
          //    li += '  <a href="' + realtime_news[i].url + '" target="_blank">';
          //    li += '    <div class="source">' + realtime_news[i].source + '</div>';
          //    li += '    <div class="title">' + realtime_news[i].title + '</div>';
          //    li += '    <div class="timeago"><time class="timeago" datetime="' + realtime_news[i].published_at + '">' + jQuery.timeago(realtime_news[i].published_at) + '</time></div>';
          //    li += '  </a></li>';
          //    $(".realtime-newsfeed").append(li);
          //  }
          //    }
          //  }
          //});

    //$scope.items = [];
    //var counter = 1;
    //$scope.loadMore = function() {
    //  News.query({offset: counter, limit: limit}, 
    //    function success(result) {
    //      console.log(result);
    //      //$scope.newsfeed.push.apply($scope.newsfeed, result);
    //    }
    //  );
    //  counter += 1;
    //};
    //
    //$scope.loadMore();

//var jendela24App = angular.module('jendela24App', []);
//
//jendela24App.controller('NewsFeedCtrl', function($scope, $http, $window, $document) {
//  
//  $http.get('http://167.205.65.43/jendela24/1.0/news/?limit=50').success(function(data) {
//    for (var i = 0; i < data.length; i++ ) {
//      data[i].timeago = jQuery.timeago(data[i].published_at);
//      data[i].summary = data[i].summary.replace('src', 'ng-src');
//    }
//    $scope.newsfeed = data;
//  });
//});

  //$(window).scroll(function() {
  //  if ($(window).scrollTop() + $(window).height() > $(document).height() - 200) {
  //    console.log("bottom!");
  //    if ($(".spinning").children().length === 0) {
  //      console.log("spinning!");
  //      var img = '<img src="/static/img/common/spin-white.gif">';
  //      $(".spinning").append(img);
  //    }
  //  }
  //});
