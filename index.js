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
app.set('view engine', "jade"); // your engine, you can use html, jade, ejs, vash, etc
app.set('port', process.env.PORT || 80); // set up the port to be production or 80.
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

app.get('/api/todos', function(req, res) {
    // if there is an error retrieving, send the error. nothing after res.send(err) will execute
    console.log("yoyoyo");
    res.json(events); // return all todos in JSON format
});

app.get('/something', function(req, res) {
  res.send('Hei, this is something!!!');
});

app.listen(app.get('port'), function(req, res) {
 console.log('Server listening at ' + app.get('port'));
});



// Serve static files

