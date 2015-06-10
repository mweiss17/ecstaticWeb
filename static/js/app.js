(function(){
	var app = angular.module('ecstatic', []);

	app.controller('StaffController', function(){
		this.users = persons;

	});

	var persons = [
	{
		name: 'Jonathan',
		age: 26,
		animal: 'Rainbow Lion',
		isHome: true,
	},
	{
		name: 'Martin',
		age: 23,
		animal: 'Space Monkey',
		isHome: true,
	}

	];

})();