'use strict';

/* Controllers */

var jendela24App = angular.module('jendela24App', []);

jendela24App.controller('NewsFeedCtrl', function($scope, $http) {
  $http.get('http://localhost/jendela24/1.0/news/?limit=50').success(function(data) {
    for (var i = 0; i < data.length; i++ ) {
      data[i].timeago = jQuery.timeago(data[i].published_at);
      data[i].summary = data[i].summary.replace('src', 'ng-src');
    }
    $scope.newsfeed = data;
  });
});

jendela24App.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
