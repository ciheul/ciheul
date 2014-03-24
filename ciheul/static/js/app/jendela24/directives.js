'use strict';

/* Directives */

var jendela24Directives = angular.module('jendela24Directives', []);

jendela24Directives.directive('whenScrolled', function($window, $document) {
//jendela24Directives.directive('whenScrolled', function() {
  console.log("whenScrolled");
  return function(scope, elm, attr) {
    var raw = elm[0];
    console.log(elm);
    console.log(raw);
    angular.element($window).bind("scroll", function() {
    //elm.bind('scroll', function() {
      console.log("scrolling bro!");
      if (raw.scrollTop + raw.offsetHeight >= raw.scrollHeight) {
        scope.$apply(attr.whenScrolled);
      }
    });
  };
});
