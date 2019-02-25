var app = angular.module('GDAdmin', []);

var config = {
    headers : {
        'Content-Type': "application/json;",
        'CrossOrigin': "anonymous",
        'Access-Control-Allow-Origin': "true"
    }
}

app.controller("GDAdminController", function($scope, $http, $window) {
  $scope.CuEmail = "John@example.cz";
  $scope.CuName = "Doe";
  $scope.CuPassword = "ss";
  $scope.CuShowError = false;
  $scope.CuError = "test";
  $scope.CreateUser = function () {
    var dest = "http://" + server_url + "/user/";
    var body = {
        'name': $scope.CuName,
        'password': $scope.CuPassword,
        'email': $scope.CuEmail
    }
    $http.post(dest, body, config).then(
        function successCallback(response) {
            $scope.CuShowError = true;
            $scope.CuError = response.data;
            $window.location.reload();
        }, function errorCallback(response) {
            $scope.CuError = "error CreateUser";
        }
    );
  };
});