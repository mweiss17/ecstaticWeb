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

    describe('post_location', function () {

        it("should post two users locations", function (done) {
            var returned_twice = false;
            socket.emit('post_location', JSON.stringify({username: "mweiss10", lat: 30.0, lon: 40.0}));
            socket.emit('post_location', JSON.stringify({username: "mykul", lat: 40.0, lon: 50.0}));
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
                done();
            });
        });
    }); 

    describe('send_text_chatlog', function() {
        it("should store a message in the chatlog", function (done) {
            socket.emit('send_text', JSON.stringify({room_number:0, message:"anyone there?"}));
            done();
        });
    });


    describe('get_rooms_around_me', function () {
        it("should get one room", function (done) {
            socket.emit('get_rooms_around_me', JSON.stringify({username: "mykul"}));
            socket.on('return_get_rooms_around_me', function (data) {
                assert.include(data.rooms[0].room_name, "testy_room");
                done();
            });
        });
    });

    describe('join_room', function () {
        it("should put two users in one room", function (done) {
            socket.emit('join_room', JSON.stringify({username: "mykul", room_number:0}));
            var returned_twice = false;
            socket.on('realtime_join_room', function (data) {
                if(returned_twice){
                    done();
                }
                else{
                    returned_twice = true;
                }
            });
            socket.on('return_join_room', function (data) {
                if(returned_twice){
                    done();
                }
                else{
                    returned_twice = true;
                }
            });
        });
    });

    describe('get_list_of_users', function () {
        it("should get two users in one room", function (done) {
            socket.emit('get_user_list', JSON.stringify({room_number:0}));
            socket.on('return_get_user_list', function (data) {
                expect(data.length).to.equal(2);
                done();
            });
        });
    });

    describe('add_song', function () {
        it("should add a song to the playlist", function (done) {
            socket.emit('add_song', JSON.stringify({room_number:0, duration:120, artwork_url:"https:test1", stream_url:"https:test1", song_name:'snow', artist:'Red Hot Chili Peppers', username:'mykul'}));
            socket.on("realtime_add_song", function (data) {
                done();
            });
        });
    });

    describe('get_playlist', function () {
        it("should get a playlist with no songs", function (done) {
            socket.emit('get_playlist', JSON.stringify({room_number:0}));
            socket.on("return_get_playlist", function (data) {
                done();
            });
        });
    });

    describe('remove_song', function () {
        it("should remove a song from the playlist", function (done) {
            socket.emit('remove_song', JSON.stringify({room_number:0, duration:120, artwork_url:"https:test1", stream_url:"https:test1", song_name:'snow', artist:'Red Hot Chili Peppers', username:'mykul'}));
            socket.on("realtime_remove_song", function (data) {
                done();
            });
        });
    });

    describe('send_text', function() {
        it("should send a realtime message to both users", function (done) {
            socket.emit('send_text', JSON.stringify({room_number:0, message:"yo does this chat work?"}));
            socket.on('realtime_send_text', function (data) {
                done();
            });
        });
    });

    describe('leave_room', function () {
        it("should remove one user from room", function (done) {
            socket.emit('leave_room', JSON.stringify({username: "mykul", room_number:0}));
            socket.on('realtime_leave_room', function (data) {
                done();
            });
        });
    });

    describe('check_unsubscribed', function () {
        it("should unsubscribe to room updates after leaving the room", function (done) {
            socket.emit('add_song', JSON.stringify({room_number:0, duration:120, artwork_url:"https:test1", stream_url:"https:test1", song_name:'snow', artist:'Red Hot Chili Peppers', username:'test'}));
            socket.on('realtime_add_song', function (data) {
                console.log("ERROR did not unsubscribe");
                done();
            });
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

