/*jslint node: true */
/*global describe: false, before: false, after: false, it: false */
"use strict";

// Declare the variables used
var expect = require('chai').expect,
    assert = require('chai').assert,
    request = require('request'),
    server = require('../index'),
    redis = require('redis'),
    io = require('socket.io-client'),
    client;
client = redis.createClient();

var socket = io.connect('http://localhost:8888', {
    'reconnection delay' : 0,
    'reopen delay' : 0,
    'force new connection' : true
}); 

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

describe('rooms api', function () {

    // Beforehand, start the server
    before(function (done) {
        //socket.emit('create_room', { username: "mweiss10", room_name:"test_room_name222" });
        //socket.emit('create_room', { username: "mykul", room_name:"test_room_name" });
        //request('http://54.173.157.204/geo/post_location/?username=mweiss10&my_location_lat=90.0&my_location_lon=30.0');
        //request('http://54.173.157.204/geo/post_location/?username=mykul&my_location_lat=70.0&my_location_lon=30.0');
        done();
    });

    describe('post_loction', function () {

        it("should post two users locations", function (done) {
            var returned_twice = false;
            socket.emit('post_location', JSON.stringify({username: "mweiss10", lat: 30, lon: 40.0}));
            socket.emit('post_location', JSON.stringify({username: "mykul", lat: 40, lon: 50}));
            socket.on('return_post_location', function (data) {
                if(returned_twice){
                done();
                }
                else{
                    returned_twice = true;
                }
            });
        });
    });

    describe('create_room', function () {
        it("should create a room for one person", function(done) {
            socket.emit('create_room', JSON.stringify({username: "mweiss10", room_name: "testy_room"}));
            socket.on('return_create_room', function (data) {
                console.log(data);
                done();
            });
        });
    }); 

    describe('get_rooms_around_me', function () {

        it("should get one room", function (done) {

            socket.emit('get_rooms_around_me', JSON.stringify({username: "mykul"}));

            // Handle the message being received
            socket.on('return_get_rooms_around_me', function (data) {
                assert.include(data, "testy_room");
                done();
            });
        });
    });


    /*describe('get_playlist', function () {

        it("should get a playlist with two songs", function (done) {
            //add two songs
            socket.emit('push_song', 1, JSON.stringify({duration:120, artwork_url:"https:test1", stream_url:"https:test1", song_name:'snow', artist:'Red Hot Chili Peppers', user:'mykul'}));
            socket.emit('push_song', 1, JSON.stringify({duration:140, artwork_url:"https:test2", stream_url:"https:test2", song_name:'creep', artist:'Radiohead', user:'mweiss10'}));
            
            //create songs to use as keys (and insert the second) 
            var before = JSON.stringify({duration:120, artwork_url:"https:test1", stream_url:"https:test1", song_name:'snow', artist:'Red Hot Chili Peppers', user:'mykul'});
            var song_to_insert = JSON.stringify({duration:180, artwork_url:"https:test3", stream_url:"https:test3", song_name:'testtrack', artist:'jibbly', user:'other'});
            var song_to_remove = JSON.stringify({duration:140, artwork_url:"https:test2", stream_url:"https:test2", song_name:'creep', artist:'Radiohead', user:'mweiss10'});

            //insert one song before another
            socket.emit('insert_song', {room_number:1, before:before, song_to_insert:song_to_insert});

            //remove the other song
            socket.emit('remove_song', {room_number:1, song_to_remove:song_to_remove});

            //grab the playlist
            socket.emit('get_playlist', {room_number:1});

            // Handle the message being received
            socket.on('get_playlist', function (data) {
                var first_song = JSON.parse(data[0]);
                var second_song = JSON.parse(data[1]);
                expect(first_song.duration).to.equal(180);
                expect(second_song.duration).to.equal(120);
                done();
            });
        });
    });


    describe("playlist_update", function(){
        it("should get an update", function (done) {
            //subscribe
            socket.emit("subscribe_to_playlist", {room_number:1});
            //publish
            socket.emit("publish_to_playlist", {room_number:1, message:"do a thing"});
            //check update
            socket.on(":1:room:1:playlist_channel", function (data){
                expect(data).to.include("do a thing");
                done();
            });
        });
    });*/


    
    // Afterwards, stop the server and empty the database
    after(function (done) {
        console.log('Stopping the server');
        client.flushdb();
        done();
    });

});

