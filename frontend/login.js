// Ensure you are fetching the existing module
var app = angular.module('userApp');

app.controller('LoginController', function($scope, $http, $window, $timeout) {
    $scope.credentials = {};
    $scope.errorMessage = "";
    $scope.successMessage = "";

    // DOUBLE CHECK: Does your Django urls.py have 'api/login/' or just 'login/'?
    const loginApiUrl = 'http://127.0.0.1:8000/login/'; 

    $scope.login = function() {
        $scope.errorMessage = "";
        $scope.successMessage = "";

        // Log the data to see what is being sent (Check browser console)
        console.log("Sending credentials:", $scope.credentials);

        $http.post(loginApiUrl, $scope.credentials)
            .then(function(response) {
                $scope.successMessage = "Login successful! Redirecting...";
                
                // Store user data
                localStorage.setItem('currentUser', JSON.stringify(response.data.user));
                
                $timeout(function() {
                    $window.location.href = 'index.html'; 
                }, 2000);
            })
            .catch(function(error) {
                console.error("Login error details:", error);
                
                // Handle specific 400 error messages from Django
                if (error.status === 400) {
                    $scope.errorMessage = error.data.error || "Missing email or password.";
                } else if (error.status === 401 || error.status === 404) {
                    $scope.errorMessage = "Invalid email or password.";
                } else {
                    $scope.errorMessage = "Server error (Status " + error.status + "). Please try again.";
                }
            });
    };
});