var app = angular.module('ecstatic', []);

app.controller('mainController',['$scope', '$http', function($scope, $http) {
//    $scope.test = "testytest";
    // when landing on the page, get all todos and show them
    $http.get('/api/upcomingEvents')
        .success(function(data) {
            $scope.upcomingEvents = data;
            $scope.playlist = data.playlist;
            display_countdown(data.start_time);
            console.log(data);
        })
        .error(function(data) {
            console.log('Error: ' + data);
        });
}]);