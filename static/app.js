angular.module('mbiApp', [])

.config(['$interpolateProvider', function ($interpolateProvider) {
    //change handlebars notation so that angular plays well with flask
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
}])

.controller('mbiCtrl', ['$scope', '$http', function($scope, $http) {

    $scope.generate = function generate() {
        delete $scope.valid;
        delete $scope.errors;

        $http.get('/generate').then(function (r) {
            $scope.mbi = r.data;
        })
    }

    $scope.validate = function validate() {
        $http.post('/verify', {mbi: $scope.mbi}).then(function (r) {
            $scope.valid = r.data.valid;
            $scope.errors = r.data.errors;

        }, function (err) {
            $scope.valid = false;
            $scope.errors = [err];
        })
    }

    $scope.continuousVerification = false;

    $scope.$watch('mbi', function() {
        if ($scope.continuousVerification) {
            $scope.validate();
        }
    })
}]);