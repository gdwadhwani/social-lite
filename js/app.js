
    var app = angular.module('socialLite', []);

    app.controller('EventController', function(){
        this.eventItems = events;
    });

    app.controller('UserController', function () {
        this.userInfo = currentUser;
    });

    var currentUser = {
        userid: "100001userid",
        password: "test password",
        displayname: "test user displayname",
        email_address: "huangbq.01@gmail.com",
        location: "college park, MD",
        hometown: "Shanghai, China",
        language: ["English","Chinese"],
        birthday: "1989-04-11",
        gender: "male",
        bio: "I'm interested in everything! I'm a test user!",
        interests: [{
            name: "Social Media",
            parent: "Internet & Technology"
        },
        {
            name: "Interaction Design",
            parent: "Internet & Technology"
        },
        {
            name: "Cloud Computing",
            parent: "Internet & Technology"
        }],
        facebook_url: "www.facebook.com/test-user-facebook",
        twitter_url: "www.twitter.com/test-user-twitter"
    };

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

    var all_interests = [{
            name: "Art",
            parent: "Arts & Entertainment"
        },
        {
            name: "Fiction",
            parent: "Arts & Entertainment"
        },
        {
            name: "Film",
            parent: "Arts & Entertainment"
        },
        {
            name: "Lean Startup",
            parent: "Business & Career"
        },
        {
            name: "Marketing",
            parent: "Business & Career"
        },
        {
            name: "Investing",
            parent: "Business & Career"
        },
        {
            name: "Social Media",
            parent: "Internet & Technology"
        },
        {
            name: "Interaction Design",
            parent: "Internet & Technology"
        },
        {
            name: "Cloud Computing",
            parent: "Internet & Technology"
        }];