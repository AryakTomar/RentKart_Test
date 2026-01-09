angular.module('categoryApp', [])
.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}])
.controller('CategoryController', function($scope, $http) {
    const API_URL = 'http://127.0.0.1:8000/categories/';
    $scope.categories = [];
    $scope.newCategory = {};

    $scope.loadCategories = function() {
        $http.get(API_URL).then(function(res) {
            $scope.categories = res.data;
        });
    };

    $scope.addCategory = function() {
        $http.post(API_URL, $scope.newCategory).then(function(res) {
            $scope.categories.push(res.data);
            $scope.newCategory = {};
        });
    };

    // MATCH THESE NAMES TO THE HTML ng-click
    $scope.editCategory = function(cat) {
        cat.original = angular.copy(cat);
        cat.editing = true;
    };

    $scope.cancelEdit = function(cat) {
        angular.copy(cat.original, cat);
        cat.editing = false;
    };

    $scope.saveCategory = function(cat) {
        $http.put(API_URL + cat.id + '/', cat).then(function() {
            cat.editing = false;
        });
    };

    $scope.deleteCategory = function(cat) {
        if (confirm('Delete this category?')) {
            $http.delete(API_URL + cat.id + '/').then(function() {
                $scope.categories.splice($scope.categories.indexOf(cat), 1);
            });
        }
    };

    $scope.loadCategories();
});