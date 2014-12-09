(function(){
    var app = angular.module('socialLite', []);

    app.controller('EventController',['$http', '$log', function($http, $log, $scope){
//        this.eventItems = events;
        var eventCtrl = this;
        eventCtrl.eventItems = [];

        $http.get('/all-events').success(function(data){
            eventCtrl.eventItems = data;
        });
    }]);

    app.controller('UserController', function ($scope) {
        this.currentUser = currentUserInfo;
        this.allInts = all_interests;
        this.parentInts = ["Arts & Entertainment", "Business & Career", "Internet & Technology"];

        $scope.cate1 = "Arts & Entertainment";
        $scope.cate2 = "Business & Career";
        $scope.cate3 = "Internet & Technology";

        this.updateUserInfo = function(){

            debugger;
        };
    });
    app.filter('getCatedInts', function () {
      return function (items, cate) {
        var filtered = [];
        for (var i = 0; i < items.length; i++) {
          var item = items[i];
          if (item.parent === cate) {
            filtered.push(item);
          }
        }
        return filtered;
      };
    });



    var currentUserInfo = {
        userid: "100001userid",
        password: "test password",
        displayname: "test user displayname",
        email_address: "huangbq.01@gmail.com",
        location: "college park, MD",
        age: "25",
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
    }];

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

    var event_details = {
        eventid: "123123",
        name: "Empowering Mobile Development with Angular",
        location: "123 Test Rd, college park, MD",
        description: 'A discussion of some of the core technologies we use at Nudge to enable Angular-based JS/HTML5 applications to "feel native", including PhoneGap/Cordova, ngTouch, and "notifying" promises with local data for lightning-fast response times. The talk should hopefully be useful to anyone interested in pursuing PhoneGap apps, mobile web development, and anyone looking to make their Angular apps feel more responsive.'
    };

    var attender_list = {
        eventid : "123123",
        attenders: [{
            userid: "100001userid",
            name: "test user"
        },
        {
            userid: "100002userid",
            name: "test user2"
        },{
            userid: "100003userid",
            name: "test user3"
        }]
    };

    app.directive('checklistModel', ['$parse', '$compile', function($parse, $compile) {
      // contains
      function contains(arr, item) {
        if (angular.isArray(arr)) {
          for (var i = 0; i < arr.length; i++) {
            if (angular.equals(arr[i], item)) {
              return true;
            }
          }
        }
        return false;
      }

      // add
      function add(arr, item) {
        arr = angular.isArray(arr) ? arr : [];
        for (var i = 0; i < arr.length; i++) {
          if (angular.equals(arr[i], item)) {
            return arr;
          }
        }
        arr.push(item);
        return arr;
      }

      // remove
      function remove(arr, item) {
        if (angular.isArray(arr)) {
          for (var i = 0; i < arr.length; i++) {
            if (angular.equals(arr[i], item)) {
              arr.splice(i, 1);
              break;
            }
          }
        }
        return arr;
      }

      function postLinkFn(scope, elem, attrs) {
        // compile with `ng-model` pointing to `checked`
        $compile(elem)(scope);

        // getter / setter for original model
        var getter = $parse(attrs.checklistModel);
        var setter = getter.assign;

        // value added to list
        var value = $parse(attrs.checklistValue)(scope.$parent);

        // watch UI checked change
        scope.$watch('checked', function(newValue, oldValue) {
          if (newValue === oldValue) {
            return;
          }
          var current = getter(scope.$parent);
          if (newValue === true) {
            setter(scope.$parent, add(current, value));
          } else {
            setter(scope.$parent, remove(current, value));
          }
        });

        // watch original model change
        scope.$parent.$watch(attrs.checklistModel, function(newArr, oldArr) {
          scope.checked = contains(newArr, value);
        }, true);
      }

      return {
        restrict: 'A',
        priority: 1000,
        terminal: true,
        scope: true,
        compile: function(tElement, tAttrs) {
          if (tElement[0].tagName !== 'INPUT' || !tElement.attr('type', 'checkbox')) {
            throw 'checklist-model should be applied to `input[type="checkbox"]`.';
          }

          if (!tAttrs.checklistValue) {
            throw 'You should provide `checklist-value`.';
          }

          // exclude recursion
          tElement.removeAttr('checklist-model');

          // local scope var storing individual checkbox model
          tElement.attr('ng-model', 'checked');

          return postLinkFn;
        }
      };
    }]);
}());