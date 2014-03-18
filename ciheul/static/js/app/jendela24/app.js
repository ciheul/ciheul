'use strict';

/* App Module */

var jendela24App = angular.module('jendela24App', [
  'ngRoute', 
  'jendela24Controllers', 
  'jendela24Services'
]);

jendela24App.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');

});

jendela24App.config(['$routeProvider', 
  function($routeProvider) {
    $routeProvider.
      when('/', {
        controller: 'NewsFeedCtrl',
        templateUrl: '/static/partials/jendela24/newsfeed.html'
      });
//      otherwise({
//        redirectTo: '/'
//      });
  }
]);
