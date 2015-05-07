/*jslint node: true */
/*global describe: false, before: false, after: false, it: false */
"use strict";

// Declare the variables used
var expect = require('chai').expect,
    request = require('request'),
    server = require('../index'),
    redis = require('redis'),
    io = require('socket.io-client'),
    client;
client = redis.createClient();

// Server tasks
describe('server', function () {
    // Test the index route
    describe('Test the index route', function () {
        it('should return a page with the title Babblr', function (done) {
            request.get({ url: 'http://localhost:8888/' }, function (error, response, body) {
                expect(body).to.include('Babblr');
                expect(response.statusCode).to.equal(200);
                expect(response.headers['content-type']).to.equal('text/html; charset=utf-8');
                done();
            });
        });
    });
});

// Test sending a message
describe('get_rooms_around_me', function () {
    // Connect to server
    var socket = io.connect('http://localhost:8888', {
        'reconnection delay' : 0,
        'reopen delay' : 0,
        'force new connection' : true
    }); 

    // Beforehand, start the server
    before(function (done) {
        console.log('preparing test data');
        socket.emit('create_room', { username: "mweiss10", room_name:"test_room_name222" });
        socket.emit('create_room', { username: "mykul", room_name:"test_room_name" });
        request('http://54.173.157.204/geo/post_location/?username=mweiss10&my_location_lat=90.0&my_location_lon=30.0');
        request('http://54.173.157.204/geo/post_location/?username=mykul&my_location_lat=70.0&my_location_lon=30.0');
        done();
    });


    it("should get the rooms around me", function (done) {
        socket.emit('get_rooms_around_me');

        // Handle the message being received
        socket.on('get_rooms_around_me', function (data) {
            console.log("in test");
            console.log(data);
            //expect(data).to.include('user');
            socket.disconnect();
            done();
        });
    });

    // Afterwards, stop the server and empty the database
    after(function (done) {
        console.log('Stopping the server');
        client.flushdb();
        done();
    });


});

