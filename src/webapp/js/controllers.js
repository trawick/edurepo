var ejectiveApp = angular.module('ejectiveApp', []);

ejectiveApp.run(function($rootScope) {
    $rootScope.$on('updateTeacherEmailEvent', function(event, args) {
        $rootScope.$broadcast('handleTeacherEmailBroadcast', args);
    });
});

ejectiveApp.controller('GetTeacherEmailCtrl', function ($scope) {

    $scope.update = function(teacherEmail) {
        $scope.$emit('updateTeacherEmailEvent', teacherEmail);
    };

});

ejectiveApp.controller('EdjectiveCtrl', function ($scope, $http) {

    $scope.$on('handleTeacherEmailBroadcast', function(event, args) {
        $scope.edjective = {snippet: 'loading ' + args + '...'};

        $http.get('http://127.0.0.1:8000/teachers/api/teacher_class/?format=json&teacher__email=' + args).success(function(data) {
            if (data.meta.total_count == 0) {
                $scope.edjective = {snippet: 'Invalid teacher e-mail address!'};
            }
            else {
                $scope.edjective = {snippet: data.objects[0].name + " (" + data.objects[0].course_id + ")"};
            }
        });
    });
});
