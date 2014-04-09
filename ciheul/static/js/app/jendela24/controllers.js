'use strict';

/* Controllers */

var jendela24Controllers = angular.module('jendela24Controllers', ['ui.bootstrap']);

jendela24Controllers.controller('NewsFeedCtrl', ['$scope', '$modal', 'News',
  function($scope, $modal, News) {
    var limit = 20;
    $scope.newsfeed = News.query({offset: 0, limit: limit});

    var counter = limit;
    $(window).scroll(function() {
      //if ($(window).scrollTop() + $(window).height() > $(document).height() - 10) {
      if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        console.log("bottom!");
        if ($(".spinning").children().length === 0) {
          console.log("spinning!");
          var img = '<img src="/static/img/common/spin-white.gif">';
          $(".spinning").append(img);

          News.query({offset: counter, limit: limit}, 
            function success(result) {
              for (var i = 0; i < result.length; i++) {      
                //var li = generateElementLi(result[i].url, result[i].source, 
                //  result[i].title, result[i].published_at);
                var li  = '<li class="news" ng-click="showDetailNews()"><a href="' + result[i].url + '" target="_blank">';
                    li += '  <div class="source">' + result[i].source + '</div>';
                    li += '  <div class="title">' + result[i].title + '</div>';
                    li += '  <div class="timeago"><time class="timeago" datetime="' + result[i].published_at + '">' + jQuery.timeago(result[i].published_at) + '</time></div>';
                    li += '</a></li>';
                $(".newsfeed").append(li);
              }
              $(".news").click(function() {
                $scope.showDetailNews();
              });
              $(".spinning").remove();
            }
          );
          counter += limit;
        }
      }
    });

    $scope.showDetailNews = function() {
      var summary = $(this)[0].news.summary;
      var title = $(this)[0].news.title;
      var modalDetailNews = $modal.open({
        templateUrl: '/static/partials/jendela24/detail_news_modal.html',
        controller: ModalDetailNewsCtrl,
        resolve: {
          title: function() {return title;},
          summary: function() {return summary;}
        }
      });
      
    };
  }]
);

var ModalDetailNewsCtrl = function($scope, $modalInstance, title, summary) {
  $scope.title = title;
  $scope.summary = summary;

  $scope.cancel = function() {
    $modalInstance.dismiss('cancel');
  };
  console.log(summary);
};
//function generateElementLi(url, source, title, published_at) {
//  var li  = '<li class="news" ng-click="showDetailNews()"><a href="' + url + '" target="_blank">';
//      li += '  <div class="source">' + source + '</div>';
//      li += '  <div class="title">' + title + '</div>';
//      li += '  <div class="timeago"><time class="timeago" datetime="' + published_at + '">' + jQuery.timeago(published_at) + '</time></div>';
//      li += '</a></li>';
//  return li;
//}

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

var ModalInstanceCtrl = function($scope, $http, $modalInstance, items) {
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

  $scope.login_twitter = function() {
    $http({
      method: 'POST', 
      url: 'https://api.twitter.com/oauth/request_token',
      config: {
        headers: {
          'oauth_callback': 'http://localhost:8000/jendela24/login/redirect',
          'oauth_consumer_key': 'kGRMC2Y3RyGde0fsP3s9pg',
          'oauth_signature_method': 'HMAC-SHA1',
          'oauth_version': '1.0',
          'Access-Control-Allow-Origin': 'https://api.twitter.com'
        }
      },
    }).success(function(data) {
        console.log("success");
      }).
      error(function(data, status, header, config) {
        console.log("error" + status);
        console.log(header);
        console.log(config);
      });
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
