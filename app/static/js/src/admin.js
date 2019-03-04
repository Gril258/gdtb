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
  $scope.Init = function() {
    $scope.GetTaskList()
    $scope.GetUserList()
  }

  $scope.GetTaskList = function () {
    var dest = "http://" + server_url + "/task/";
    $http.get(dest, config).then(
        function successCallback(response) {
            $scope.TaskList = response.data;
        }, function errorCallback(response) {
            $scope.HttpError = response.code;
        }
    );
  }

  $scope.GetUserList = function () {
    var dest = "http://" + server_url + "/user/";
    $http.get(dest, config).then(
        function successCallback(response) {
            $scope.UserList = response.data;
        }, function errorCallback(response) {
            $scope.HttpError = response.code;
        }
    );
  }

  $scope.DeleteUser = function (userId) {
    var dest = "http://" + server_url + "/user/" + userId;
    $http.delete(dest, config).then(
        function successCallback(response) {
            $scope.GetUserList()
        }, function errorCallback(response) {
            $scope.HttpError = response.code;
        }
    );
  }

  $scope.CreateTask = function () {
    var dest = "http://" + server_url + "/task/";
    var body = {
        'name': $scope.CtName,
        'status': $scope.CtStatus,
        'module': $scope.CtModule,
        'data': $scope.CtData,
        'options': $scope.CtOptions
    }
    $http.post(dest, body, config).then(
        function successCallback(response) {
            $scope.GetTaskList()
        }, function errorCallback(response) {
            $scope.CuError = "error CreateUser";
        }
    );
  };

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
            $scope.GetUserList()
        }, function errorCallback(response) {
            $scope.CuError = "error CreateUser";
        }
    );
  };
});