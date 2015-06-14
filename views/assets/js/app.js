var app = angular.module('ecstatic', 
	[        
		"ngSanitize",
    "plangular",
    "ngAnimate"
	]
)
.config(function(plangularConfigProvider){
    plangularConfigProvider.clientId = '96c11abd04d7d34dc518d9f3ec10a2bc';
})
.controller('mainController',['$scope', '$http', function($scope, $http) {
      $http.get('/api/upcomingEvents')
      .success(function(data) {
          $scope.upcomingEvents = data;
          $scope.server_playlist = data.playlist;
          display_countdown(data.start_time);
          console.log(data);
      })
      .error(function(data) {
          console.log('Error: ' + data);
      });

      $http.get('/api/sync')
      .success(function(data) {
          var timeOfReturn = new Date().getTime();
          var json = JSON.parse(data);
          if(json.elapsedTime > 0){
            console.log("need to sync");
            $scope.elapsedTimeJson = JSON.stringify({timeOfReturn : timeOfReturn, elapsedTime: json.elapsedTime});
            $scope.syncObj = json;
            //$scope.index = json.index;
          }
          else{
            $scope.showButton = "hidden";
            console.log("event hasn't started");
          }
      })
      .error(function(data) {
          console.log('Error: ' + data);
      });

    $scope.syncClick = function(){
        console.log("hey");
    };


}])

function display_countdown(start_time){
    console.log("display counter start_time="+start_time);
	countdown(start_time, function(ts){
		document.getElementById('counter').innerHTML = ts.toHTML();

	}, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
}
