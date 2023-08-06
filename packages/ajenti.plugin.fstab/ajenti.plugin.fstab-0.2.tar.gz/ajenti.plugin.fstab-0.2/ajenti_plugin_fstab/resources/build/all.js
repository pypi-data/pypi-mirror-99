'use strict';

// the module should depend on 'core' to use the stock services & components
angular.module('ajenti.fstab', ['core']);


'use strict';

angular.module('ajenti.fstab').config(function ($routeProvider) {
    $routeProvider.when('/view/fstab', {
        templateUrl: '/fstab:resources/partial/index.html',
        controller: 'FstabIndexController'
    });
});


'use strict';

angular.module('ajenti.fstab').controller('FstabIndexController', function ($scope, $http, pageTitle, gettext, notify, messagebox) {
    pageTitle.set(gettext('Fstab'));

    $scope.showDetails = false;
    $scope.add_new = false;

    $http.get('/api/get_mounted').then(function (resp) {
        $scope.mounted = resp.data;
    });

    $scope.umount = function (entry) {
        $http.post('/api/umount', { mountpoint: entry.mountpoint }).then(function (resp) {
            notify.success(gettext('Device successfully unmounted!'));
            position = $scope.mounted.indexOf(entry);
            $scope.mounted.splice(position, 1);
        });
    };

    $http.get('/api/fstab').then(function (resp) {
        $scope.fstab = resp.data.filesystems;
    });

    $scope.edit = function (device) {
        $scope.edit_device = device;
        $scope.showDetails = true;
    };

    $scope.save = function () {
        $scope.showDetails = false;
        $http.post('/api/fstab', { config: $scope.fstab }).then(function (resp) {
            notify.success(gettext('Fstab successfully saved!'));
        });
    };

    $scope.add = function () {
        $scope.add_new = true;
        $scope.edit_device = {
            'device': '',
            'mountpoint': '/',
            'type': 'ext4',
            'options': 'defaults',
            'freq': '0',
            'passno': '0'
        };
        $scope.showDetails = true;
    };

    $scope.saveNew = function () {
        $scope.reset();
        $scope.fstab.push($scope.edit_device);
        $scope.save();
    };

    $scope.remove = function (device) {
        messagebox.show({
            text: gettext('Do you really want to permanently delete this entry?'),
            positive: gettext('Delete'),
            negative: gettext('Cancel')
        }).then(function () {
            position = $scope.fstab.indexOf(device);
            $scope.fstab.splice(position, 1);
            $scope.save();
        });
    };

    $scope.reset = function () {
        $scope.showDetails = false;
        $scope.add_new = false;
    };
});


