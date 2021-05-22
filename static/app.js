angular.module('mbiApp', [])

    .config(['$interpolateProvider', function($interpolateProvider) {
        //change handlebars notation so that angular plays well with flask
        $interpolateProvider.startSymbol('{[{');
        $interpolateProvider.endSymbol('}]}');
    }])

    .controller('mbiCtrl', ['$scope', '$http', function($scope, $http) {

        $scope.generate = function generate() {
            $http.get('/generate').then(function (r) {
                $scope.mbi = r.data;
            })
        }

        $scope.validate = function validate() {
            $http.post('/verify', {mbi: $scope.mbi}).then(function (r) {
                $scope.valid = r.data.valid;
                $scope.error = r.data.error;

            }, function (err) {
                $scope.valid = false;
                $scope.error = err;
            })
        }
    }]);