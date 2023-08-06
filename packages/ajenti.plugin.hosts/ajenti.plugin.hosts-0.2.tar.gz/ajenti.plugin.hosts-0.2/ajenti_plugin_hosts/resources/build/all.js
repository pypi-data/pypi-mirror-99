'use strict';

// the module should depend on 'core' to use the stock services & components
angular.module('ajenti.hosts', ['core']);


'use strict';

angular.module('ajenti.hosts').config(function ($routeProvider) {
    $routeProvider.when('/view/hosts', {
        templateUrl: '/hosts:resources/partial/index.html',
        controller: 'HostsIndexController'
    });
});


'use strict';

angular.module('ajenti.hosts').controller('HostsIndexController', function ($scope, $http, pageTitle, gettext, notify, messagebox) {
    pageTitle.set(gettext('Hosts'));

    $scope.showDetails = false;
    $scope.add_new = false;

    $http.get('/api/hosts').then(function (resp) {
        $scope.hosts = resp.data.hosts;
    });

    $scope.edit = function (host) {
        if (!$scope.has_empty_alias(host)) {
            $scope.add_alias(host);
        }
        $scope.edit_host = host;
        $scope.showDetails = true;
    };

    $scope.save = function () {
        $scope.showDetails = false;
        $http.post('/api/hosts', { config: $scope.hosts }).then(function (resp) {
            notify.success(gettext('Hosts successfully saved!'));
        });
    };

    $scope.add = function () {
        $scope.add_new = true;
        $scope.edit_host = {
            'address': '127.0.0.1',
            'name': 'localhost',
            'aliases': [{ 'name': '' }]
        };
        $scope.showDetails = true;
    };

    $scope.has_empty_alias = function (host) {
        var _iteratorNormalCompletion = true;
        var _didIteratorError = false;
        var _iteratorError = undefined;

        try {
            for (var _iterator = host.aliases[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                alias = _step.value;

                if (alias.name == '') {
                    return true;
                }
            }
        } catch (err) {
            _didIteratorError = true;
            _iteratorError = err;
        } finally {
            try {
                if (!_iteratorNormalCompletion && _iterator.return) {
                    _iterator.return();
                }
            } finally {
                if (_didIteratorError) {
                    throw _iteratorError;
                }
            }
        }

        return false;
    };

    $scope.add_alias = function (host) {
        host.aliases.push({ 'name': '' });
    };

    $scope.saveNew = function () {
        $scope.reset();
        $scope.hosts.push($scope.edit_host);
        $scope.save();
    };

    $scope.remove = function (host) {
        messagebox.show({
            text: gettext('Do you really want to permanently delete this entry?'),
            positive: gettext('Delete'),
            negative: gettext('Cancel')
        }).then(function () {
            position = $scope.hosts.indexOf(host);
            $scope.hosts.splice(position, 1);
            $scope.save();
        });
    };

    $scope.reset = function () {
        $scope.showDetails = false;
        $scope.add_new = false;
    };
});


