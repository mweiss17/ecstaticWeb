var elapsed = 100;
var trackIndex = 0;
var timeOfReturn = 0;
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
            countdown(data.start_time, function(ts){
              console.log(ts);
              console.log(ts.seconds);
              $scope.seconds = ts.seconds;
              $scope.minutes = ts.minutes;
              $scope.hours = ts.hours;
              console.log("ts.toString="+ts.value/1000);
            }, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
          console.log(data);
      })
      .error(function(data) {
          console.log('Error: ' + data);
      });

      $http.get('/api/sync')
      .success(function(data) {
          timeOfReturn = new Date().getTime();
          var json = JSON.parse(data);
          if(json.elapsedTime > 0){
            elapsed = json.elapsedTime;

            //FOR GETTING THE ACTUAL TRACK INDEX
            trackIndex = json.trackIndex;

            //FOR TESTING
            //trackIndex = 1;
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

