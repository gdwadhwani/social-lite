var app = angular.module("event-directives", []);

app.directive("eventList", function () {
    return {
        restrict: 'E',
        templateUrl: 'event-list.html',
        controller: function ($scope) {

        },
        controllerAs: 'elistCtrl'
    };
});

app.directive("eventItem", function () {
    return {
        restrict: "E",
        templateUrl: "event-item.html",
        controller: function () { 

        },
        controllerAs: 'eitemCtrl'
    };
});