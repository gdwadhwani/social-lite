
    var app = angular.module('socialLite', []);

    app.controller('EventController', function(){
        this.eventItems = events;
    });

    app.directive("eventItem", function(){
        return {
            restrict: "E",
            templateUrl: "event-item.html",
        };
    });

    var events = [{
        name: "DC wine hangout",
        thumbnail: "img/1.jpg",
        caption: "The wine Caption"
    },{
        name: "DC game hangout",
        thumbnail: "img/2.jpg",
        caption: "The game strings"
    },{
        name: "Maryland football meetup",
        thumbnail: "img/3.jpg",
        caption: "football YESSSS!"
    },{
        name: "Maryland basketball meetup",
        thumbnail: "img/4.jpg",
        caption: "GET A DUNK!"
    },
    ];
