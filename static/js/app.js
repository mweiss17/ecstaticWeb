var app = angular.module('ecstatic', []);

app.controller('mainController',['$scope', '$http', function($scope, $http) {
    $scope.test = "testytest";
    // when landing on the page, get all todos and show them
    $http.get('/api/todos')
        .success(function(data) {
            $scope.todos = data;
            
            console.log(data);
        })
        .error(function(data) {
            console.log('Error: ' + data);
        });
}]);