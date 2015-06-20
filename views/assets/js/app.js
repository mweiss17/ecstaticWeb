var elapsed = 100;
var trackIndex = 0;
var timeOfReturn = 0;

//Google Analytics
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-64135413-1', 'auto');
  ga('send', 'pageview');

var app = angular.module('ecstatic', 
	[        
		"ngSanitize",
    "plangular",
    "ngAnimate",
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
              console.log("ts.value="+ts.value);
              
              //every second
              if(!$scope.$$phase) {
                console.log("$scope.trackIndex = trackIndex;"+trackIndex);
                $scope.trackIndex = trackIndex;
                $scope.$apply() 
              }


              if(ts.value < -2000){
                $scope.showButton = "hidden";
              }
              else{
                console.log("shown");
                //not hidden
                $scope.currentlyPlaying = "hidden";
                $scope.showButton = "asdfasdfsdf";
              }

              document.getElementById('seconds').innerHTML = ts.seconds.toString();
              document.getElementById('minutes').innerHTML = ts.minutes.toString();
              document.getElementById('hours').innerHTML = ts.hours.toString();
            }, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
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

            // updates the playlist's selected track
            console.log("trackIndex="+trackIndex);
            $scope.trackIndex = trackIndex;

            //FOR TESTING
            //trackIndex = 1;
          }
          else{
            console.log("event hasn't started");
          }
      })
      .error(function(data) {
          console.log('Error: ' + data);
      });

    $scope.update_selected_track = function(index){
        $scope.trackIndex = index;
        if(!$scope.$$phase) {
          $scope.$apply() 
        }
    }
}]);

/*function update_selected_track(index){
  $scope.trackIndex = index;
  if(!$scope.$$phase) {
    $scope.$apply() 
  }
}*/
function display_countdown(start_time){
    console.log("display counter start_time="+start_time);
  countdown(start_time, function(ts){
    //document.getElementById('counter').innerHTML = ts.toString();
    console.log("ts.toString="+ts.value/1000);
  }, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
}


