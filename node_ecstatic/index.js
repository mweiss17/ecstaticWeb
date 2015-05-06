/*jslint node: true */
'use strict';

// Declare variables used
var app, base_url, client, express, hbs, io, port, rtg, subscribe;

// Define values
express = require('express');
app = express();
port = process.env.PORT || 8888;
base_url = process.env.BASE_URL || 'http://localhost:8888';
hbs = require('hbs');

// Set up connection to Redis
/* istanbul ignore if */
if (process.env.REDISTOGO_URL) {
    rtg  = require("url").parse(process.env.REDISTOGO_URL);
    client = require("redis").createClient(rtg.port, rtg.hostname);
    subscribe = require("redis").createClient(rtg.port, rtg.hostname);
    client.auth(rtg.auth.split(":")[1]);
    subscribe.auth(rtg.auth.split(":")[1]);
} else {
    client = require('redis').createClient();
    subscribe = require('redis').createClient();
}

// Set up templating
app.set('views', __dirname + '/views');
app.set('view engine', "hbs");
app.engine('hbs', require('hbs').__express);

// Register partials
hbs.registerPartials(__dirname + '/views/partials');

// Set URL
app.set('base_url', base_url);

// Define index route
app.get('/', function (req, res) {
    res.render('index');
});

// Serve static files
app.use(express.static(__dirname + '/static'));

// Listen
io = require('socket.io')({
}).listen(app.listen(port));
console.log("Listening on port " + port);

// Handle new messages
io.sockets.on('connection', function (socket) {
    // Subscribe to the Redis channel
    subscribe.subscribe('ChatChannel');

    // Handle incoming messages
    socket.on('send', function (data) {
        // Publish it
        client.publish('ChatChannel', data.message);
    });

    // Handle receiving messages
    var callback = function (channel, data) {
        socket.emit('message', data);
    };
    subscribe.on('message', callback);

    // Handle disconnect
    socket.on('disconnect', function () {
        subscribe.removeListener('message', callback);
    });
});

