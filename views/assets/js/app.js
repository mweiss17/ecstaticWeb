var app = angular.module('ecstatic', 
	[        
		"ngSanitize",
        "plangular"
	]
)
.config(function(plangularConfigProvider){
    plangularConfigProvider.clientId = '96c11abd04d7d34dc518d9f3ec10a2bc';
})
.controller('mainController',['$scope', '$http', function($scope, $http) {
    console.log($scope.$$childScope);
    $scope.syncClick = function(){
        console.log("hey");
    };
}])
.factory('plangular', function() {
  var plangular;
  console.log("asdf"+plangular);
  // factory function body that constructs shinyNewServiceInstance
  return plangular;
});


function display_countdown(start_time){
    console.log("display counter start_time="+start_time);
	countdown(start_time, function(ts){
		document.getElementById('counter').innerHTML = ts.toHTML();

	}, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, 3);
}
