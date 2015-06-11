var app = angular.module('ecstatic', 
	[        
		"ngSanitize",
		"com.2fdevs.videogular",
		"com.2fdevs.videogular.plugins.controls",
        "plangular"
	]
)
.config(function(plangularConfigProvider){
    plangularConfigProvider.clientId = '96c11abd04d7d34dc518d9f3ec10a2bc';
})
.controller('mainController',['$scope', '$http', function($scope, $http) {
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
}])

function display_countdown(start_time){
	countdown(start_time, function(ts){
		document.getElementById('counter').innerHTML = ts.toHTML();

	}, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
}
