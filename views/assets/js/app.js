//
var elapsed = 100;
var trackIndex = 0;
var timeOfReturn = 0;

//Google Analytics, don't touch!
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', 'UA-64135413-1', 'auto');
  ga('send', 'pageview');
//end Google Analytics

//Angular Module
var app = angular.module('ecstatic', 
	[  
    //List of Libraries imported into Angular      
	"ngSanitize",
    "plangular",
    "ngAnimate",
	]
)

//configure plangular
.config(function(plangularConfigProvider){
    plangularConfigProvider.clientId = '96c11abd04d7d34dc518d9f3ec10a2bc';
})

//the Main Controller, gets info from server, updates scope for index.jade
.controller('mainController',['$scope', '$http', function($scope, $http) {

        //query index.js
        $http.get('/api/upcomingEvents')
        .success(function(data) {

            //parse the data
            $scope.upcomingEvents = data;
            $scope.server_playlist = data.playlist;
           
            //call this function every second
            countdown(data.start_time, function(ts){
                console.log("ts.value="+ts.value);
                
                //every second
                if(!$scope.$$phase) {
                  console.log("$scope.trackIndex = trackIndex;"+trackIndex);
                  $scope.trackIndex = trackIndex;
                  $scope.$apply() 
                }

                //if there are less than 2 seconds left before the event, hide the join button
                if(ts.value < -2000){
                  $scope.showButton = "hidden";
                }

                //if the event has not started, hide a label and button 
                else{
                  $scope.currentlyPlaying = "hidden";
                  $scope.showButton = "asdfasdfsdf";
                }

                //update the countdown every second
                document.getElementById('seconds').innerHTML = ts.seconds.toString();
                document.getElementById('minutes').innerHTML = ts.minutes.toString();
                document.getElementById('hours').innerHTML = ts.hours.toString();
              }, 
          countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
      })
      .error(function(data) {
          console.log('Error: ' + data);
      });

      //query index.js
      $http.get('/api/sync')
      .success(function(data) {
          timeOfReturn = new Date().getTime();
          var json = JSON.parse(data);
          console.log("http.get('/api/sync'), timeOfReturn = "+ timeOfReturn);
          console.log("http.get('/api/sync'), json = "+ data);
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