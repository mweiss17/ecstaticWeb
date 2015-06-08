'use strict';

/**
 * @ngdoc function
 * @name ecstaticApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ecstaticApp
 */
angular.module('ecstaticApp')
  .controller('MainCtrl', function ($scope) {
    $scope.awesomeThings = [
      'HTML5 Boilerplate',
      'AngularJS',
      'Karma'
    ];
  });
