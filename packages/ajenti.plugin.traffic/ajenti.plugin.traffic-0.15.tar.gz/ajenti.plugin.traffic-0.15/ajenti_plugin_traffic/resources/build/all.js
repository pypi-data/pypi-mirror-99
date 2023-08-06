'use strict';

angular.module('ajenti.traffic', ['core']);


'use strict';

angular.module('ajenti.traffic').controller('TrafficWidgetController', function ($scope, notify) {
    $scope.oldData = {};
    $scope.oldTimestamp = null;

    $scope.$on('widget-update', function ($event, id, data) {
        if (id !== $scope.widget.id || !data) {
            return;
        }
        $scope.txTotal = data.tx;
        $scope.rxTotal = data.rx;

        if ($scope.oldTimestamp) {
            var dt = (new Date().getTime() - $scope.oldTimestamp) / 1000.0;
            $scope.txSpeed = (data.tx - $scope.oldData.tx) / dt;
            $scope.rxSpeed = (data.rx - $scope.oldData.rx) / dt;
        }

        $scope.oldTimestamp = new Date().getTime();
        $scope.oldData = data;
    });
});

angular.module('ajenti.traffic').controller('TrafficWidgetConfigController', function ($scope, $http) {
    $scope.traffic = [];
    $http.get('/api/traffic/interfaces').success(function (interfaces) {
        return $scope.interfaces = interfaces;
    });
});


