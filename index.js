/*jslint node: true */
'use strict';

// Declare variables used
var ecstaticSockets, app, express, path, http, request, events;
express = require('express');
path = require('path');
app = express();
http = require('http');
request = require('request');

ecstaticSockets = require("./ecstaticSockets.js");
ecstaticSockets.setupEcstaticSockets(app);

// Set up templating
app.set('views', __dirname + '/views');
app.set('view engine', "jade"); 
app.set('port', process.env.PORT || 80); 
app.use(express.static('static'));

//SERVER STARTUP SHIT
//initialize event variable on server startup
request('http://54.173.157.204/appindex/', function (error, response, body) {
  if (!error && response.statusCode == 200) {
  	events = JSON.parse(body);
    for(var e in events) {
    	console.log(e);
    }
  }
});

app.get('/', function (req, res) {
  	res.render('index');
});

app.get('/api/upcomingEvents', function(req, res) {
    res.json({ host_username: "Internet Wizards", title: "International Startup Fest", start_time: /*June 14th, 6 AM*/1434448800000, playlist: [{title:"Deepcast vol 34", author:"Mark Macleod from Freshbooks", link:"https://soundcloud.com/djmarkmacleod/deepcast-vol-34-dj-mark", duration:3090}, {title:"the Magician", author:"Max Liese", link:"https://soundcloud.com/maxliesemusic/the-magician-sunlight-feat-years-years-max-liese-cover", duration:300}], userlist: ["anonymous squid", "anonymous monkey"]}); 
});

app.get('/something', function(req, res) {
  res.send('Hei, this is something!!!');
});

app.listen(app.get('port'), function(req, res) {
 console.log('Server listening at ' + app.get('port'));
});



// Serve static files

