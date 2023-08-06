'use strict';

angular.module('ajenti.auth.users', ['core']);

angular.module('ajenti.auth.users').run(function (customization) {
    customization.plugins.auth_users = {
        forceUID: null
    };
});


'use strict';

angular.module('core').config(function ($routeProvider) {
    $routeProvider.when('/view/auth-users', {
        templateUrl: '/auth_users:resources/partial/index.html',
        controller: 'AuthUsersIndexController'
    });
});


'use strict';

angular.module('ajenti.auth.users').controller('AuthUsersIndexController', function ($scope, $http, notify, pageTitle, config, users, passwd, customization, gettext) {
    pageTitle.set('Users');

    $scope.defaultRootPassword = '73637279707400100000000800000001f77e545afaeced51bdc33d16311ae24d900fbd462f444bce13d3c2aec489f90996523b8f779955a0f67708e0164de989c91a9a8093cd422fd5f5727018bb790f8aa36363273f5415660e7ff5c9fb9432e1f8ef5a3e35604ab9f2549aa85dbf2ca842573d25c02753bee5f0dd9c542b5ec51d58b443ad9f5e2b8dd9de8bd63a70908a1283c290bc7ccab30a3a88553ef23f5a6c25ccbe82e9f2b9ea656a6e373c33897e7b6376992de5cd00e78ed940486cd7bf0634ab1a1be2cf2f14ba2beabd55f82f5f3859ee9eea350c0a9fa9495749f0d0d6db21c5c17c742263e0e5bfb5c1c964edec1579c92ea538566151581bd06756564c21796eb61a0dd6d42b95ea5b1cdf667e0b06450622882fbf0bc7c9274903fd920368742769ee70e24a6d917afe6ba28faca235bcb83a1e22f37ee867d843b023424885623470940dd17c244a8f0ef998f29e5b680721d656c2a610609534e47ece10ea164b884d11ce983148aacf84044c5336bbc167fd28f45438'; // 'admin'

    users.load().then(function () {
        $scope.users = users;
        if (users.data.users == null) {
            users.data.users = {
                root: {
                    password: $scope.defaultRootPassword,
                    uid: 0
                }
            };
        }

        $scope.isDangerousSetup = function () {
            if (!users.data) {
                return false;
            }
            var safe = false;
            for (var username in users.data.users) {
                if (users.data.users[username].uid === 0) {
                    safe = true;
                }
            }
            return !safe;
        };

        config.getPermissions(config).then(function (data) {
            $scope.permissions = data;
            var result = [];
            for (var username in users.data.users) {
                $scope.resetPermissions(username);
                result.push(angular.extend($scope.userPermissions[username], users.data.users[username].permissions || {}));
            }
            return result;
        });
    }).catch(function () {
        return notify.error('Could not load config');
    });

    $scope.userPermissions = {};
    $scope.resetPermissions = function (username) {
        $scope.userPermissions[username] = {};
        $scope.permissions.forEach(function (permission) {
            $scope.userPermissions[username][permission.id] = permission.default;
        });
    };

    $scope.removeUser = function (username) {
        return delete users.data.users[username];
    };

    passwd.list().then(function (l) {
        $scope.systemUsers = l;

        $scope.getSystemUser = function (uid) {
            var _iteratorNormalCompletion = true;
            var _didIteratorError = false;
            var _iteratorError = undefined;

            try {
                for (var _iterator = $scope.systemUsers[Symbol.iterator](), _step; !(_iteratorNormalCompletion = (_step = _iterator.next()).done); _iteratorNormalCompletion = true) {
                    var u = _step.value;

                    if (u.uid === uid) {
                        return u;
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
        };
    });

    $scope.save = function () {
        for (var username in $scope.userPermissions) {
            if (!users.data.users[username]) {
                continue;
            }
            users.data.users[username].permissions = {};
            var _iteratorNormalCompletion2 = true;
            var _didIteratorError2 = false;
            var _iteratorError2 = undefined;

            try {
                for (var _iterator2 = $scope.permissions[Symbol.iterator](), _step2; !(_iteratorNormalCompletion2 = (_step2 = _iterator2.next()).done); _iteratorNormalCompletion2 = true) {
                    var permission = _step2.value;

                    var v = $scope.userPermissions[username][permission.id];
                    if (v !== permission.default) {
                        users.data.users[username].permissions[permission.id] = v;
                    }
                }
            } catch (err) {
                _didIteratorError2 = true;
                _iteratorError2 = err;
            } finally {
                try {
                    if (!_iteratorNormalCompletion2 && _iterator2.return) {
                        _iterator2.return();
                    }
                } finally {
                    if (_didIteratorError2) {
                        throw _iteratorError2;
                    }
                }
            }
        }

        users.save().then(function () {
            return notify.success('Saved');
        });
    };

    $scope.setPassword = function (username, password) {
        users.save().then(function () {
            return $http.post('/api/auth-users/set-password/' + username, password).then(function () {
                notify.success(gettext('Password updated'));
                users.load();
            });
        });
    };

    $scope.addUser = function (username) {
        users.data.users[username] = { uid: customization.plugins.auth_users.forceUID || 0 };
        $scope.resetPermissions(username);
        $scope.newUsername = '';
    };
});


'use strict';

angular.module('ajenti.auth.users').service('users', function ($http, $q) {
    var _this = this;

    this.load = function () {
        return $http.get("/api/auth-users/config").then(function (response) {
            return _this.data = response.data;
        });
    };

    this.save = function () {
        return $http.post("/api/auth-users/config", _this.data);
    };

    this.getPermissions = function (config) {
        return $http.post("/api/auth-users/permissions", config).then(function (response) {
            return response.data;
        });
    };

    this.data = {};

    return this;
});


