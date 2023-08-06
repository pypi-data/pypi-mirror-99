'use strict';

// the module should depend on 'core' to use the stock services & components
angular.module('ajenti.cron', ['core']);


'use strict';

angular.module('ajenti.cron').config(function ($routeProvider) {
    $routeProvider.when('/view/cron', {
        templateUrl: '/cron:resources/partial/index.html',
        controller: 'CronIndexController'
    });
});


'use strict';

angular.module('ajenti.cron').controller('CronIndexController', function ($scope, $http, $log, pageTitle, gettext, notify, messagebox) {
    pageTitle.set(gettext('Cron'));

    $scope.title = gettext('Cron');
    $scope.modifyJob = null;
    $scope.new = {
        'normal_tasks': {
            'minute': '*',
            'hour': '*',
            'day_of_month': '*',
            'month': '*',
            'day_of_week': '*',
            'command': '',
            'comment': '',
            'new': true
        },
        'special_tasks': {
            'special': '@reboot',
            'command': '',
            'comment': '',
            'new': true
        },
        'env_settings': {
            'name': '',
            'value': '',
            'comment': '',
            'new': true
        }
    };

    $scope.translate = {
        'normal_tasks': gettext('normal task'),
        'special_tasks': gettext('special task'),
        'env_settings': gettext('environment variable')
    };
    $scope.special = ['@reboot', '@yearly', '@annually', '@monthly', '@weekly', '@daily', '@hourly'];

    $scope.add = function (type, values) {
        job = angular.copy($scope.new[type]);
        $scope.modify(type, job);
    };

    $scope.remove = function (type, values) {
        messagebox.show({
            text: gettext('Do you really want to permanently delete this entry?'),
            positive: gettext('Delete'),
            negative: gettext('Cancel')
        }).then(function () {
            position = $scope.crontab[type].indexOf(values);
            $scope.crontab[type].splice(position, 1);
        });
    };

    $http.get('/api/get_crontab').then(function (resp) {
        $scope.crontab = resp.data;
    });

    $scope.modify = function (type, job) {
        $scope.modifyJob = { 'type': type, 'job': job };
    };

    $scope.closeDialog = function (type, job) {
        if (job.new) {
            delete job.new;
            $scope.crontab[type].push(job);
        }
        $scope.modifyJob = null;
    };

    $scope.reset = function () {
        $scope.modifyJob = null;
    };

    $scope.save = function () {
        $http.post('/api/save_crontab', { 'crontab': $scope.crontab }).then(function (resp) {
            notify.success(gettext('Crontab successfully saved !'));
        }, function (error) {
            $log.log('Failed to save crontab', error);
            notify.error(gettext('Failed to save crontab'));
        });
    };
});


