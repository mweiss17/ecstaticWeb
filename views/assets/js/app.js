var app = angular.module('ecstatic', 
	[        
		"ngSanitize",
		"com.2fdevs.videogular",
		"com.2fdevs.videogular.plugins.controls",
        "plangular"
	]
)
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
.controller('videoController',
        ["$scope", "$sce", function($scope, $sce) {
            this.config = {
                sources: [
              {src: $sce.trustAsResourceUrl("http://static.videogular.com/assets/audios/videogular.mp3"), type: "audio/mpeg"},
              {src: $sce.trustAsResourceUrl("http://static.videogular.com/assets/audios/videogular.ogg"), type: "audio/ogg"}
          ],
                theme: {
          url: "http://www.videogular.com/styles/themes/default/latest/videogular.css"
                }
            };
        }]
    );

function display_countdown(start_time){
	countdown(start_time, function(ts){
		document.getElementById('counter').innerHTML = ts.toHTML();

	}, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
}
