'use strict';

/**
 * @ngdoc function
 * @name ecstaticApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the ecstaticApp
 */
angular.module('ecstaticApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
