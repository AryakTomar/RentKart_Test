angular.module('customerApp', [])
.config(['$httpProvider', function($httpProvider) {
    // Required for Django CSRF protection
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.controller('CustomerController', function($scope, $http) {
    const API_URL = 'http://127.0.0.1:8000/customer/';
    $scope.customers = [];
    $scope.newCustomer = {};

    // 1. GET ALL
    $scope.loadCustomers = function() {
        $http.get(API_URL)
            .then(function(res) { $scope.customers = res.data; })
            .catch(function(err) { console.error('Load error', err); });
    };

    // 2. POST
    $scope.addCustomer = function() {
        $http.post(API_URL, $scope.newCustomer)
            .then(function(res) {
                $scope.customers.push(res.data);
                $scope.newCustomer = {};
            })
            .catch(function(err) { alert("Error adding customer: " + JSON.stringify(err.data)); });
    };

    // 3. PUT (Save)
    $scope.saveCustomer = function(customer) {
        $http.put(API_URL + customer.id + '/', customer)
            .then(function() { customer.editing = false; })
            .catch(function(err) { alert("Update failed"); });
    };

    // Edit/Cancel UI Logic
    $scope.editCustomer = function(c) {
        c.original = angular.copy(c);
        c.editing = true;
    };
    $scope.cancelEdit = function(c) {
        angular.copy(c.original, c);
        c.editing = false;
    };

    // 4. DELETE
    $scope.deleteCustomer = function(customer) {
        if (confirm('Delete this customer?')) {
            $http.delete(API_URL + customer.id + '/')
                .then(function() {
                    $scope.customers.splice($scope.customers.indexOf(customer), 1);
                });
        }
    };

    $scope.loadCustomers();
});