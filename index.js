/*jslint node: true */
'use strict';

// Declare variables used
var ecstaticSockets, app, express, path, http;
express = require('express');
path = require('path');
app = express();
http = require('http');

ecstaticSockets = require("./ecstaticSockets.js");
ecstaticSockets.setupEcstaticSockets(app);

// Set up templating
app.set('views', __dirname + '/views');
app.set('view engine', "jade"); // your engine, you can use html, jade, ejs, vash, etc
app.set('port', process.env.PORT || 80); // set up the port to be production or 80.
app.use(express.static('static'));
console.log("__dirname="+__dirname);
//app.set('env', process.env.NODE_ENV || 'development'); 


app.get('/', function (req, res) {
  res.render('index', { title: 'Hey', message: 'Hello there!'});
});

//app.get('/', function(req, res) {
  //res.send('Hello word');
//});

app.get('/something', function(req, res) {
  res.send('Hei, this is something!!!');
});

app.listen(app.get('port'), function(req, res) {
 console.log('Server listening at ' + app.get('port'));
});



// Serve static files

