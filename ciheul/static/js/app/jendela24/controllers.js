'use strict';

/* Controllers */

var jendela24App = angular.module('jendela24App', []);

jendela24App.controller('NewsFeedCtrl', function($scope, $http) {
  $http.get('http://localhost:8001/jendela24/1.0/news/?limit=5').success(function(data) {
    $scope.newsfeed = data;
  });

  $scope.phones = [
    {'name': 'Nexus S',
     'snippet': 'Fast just got faster with Nexus S.'},
    {'name': 'Motorola XOOM™ with Wi-Fi',
     'snippet': 'The Next, Next Generation tablet.'},
    {'name': 'MOTOROLA XOOM™',
     'snippet': 'The Next, Next Generation tablet.'}
  ];

  $scope.num = 2;
  $scope.name = "World";
});

jendela24App.config(function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[{');
  $interpolateProvider.endSymbol('}]}');
});
