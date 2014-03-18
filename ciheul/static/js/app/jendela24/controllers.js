'use strict';

/* Controllers */

var jendela24Controllers = angular.module('jendela24Controllers', []);

jendela24Controllers.controller('NewsFeedCtrl', ['$scope', 'News',
    function($scope, News) {
      $scope.newsfeed = News.query();
    }
]);

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
