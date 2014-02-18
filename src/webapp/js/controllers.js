var edjectiveApp = angular.module('edjectiveApp', []);

edjectiveApp.run(function($rootScope) {
    $rootScope.$on('updateTeacherEmailEvent', function(event, args) {
        $rootScope.$broadcast('handleTeacherEmailBroadcast', args);
    });
});

edjectiveApp.controller('GetTeacherEmailCtrl', function ($scope) {

    $scope.update = function(teacherEmail) {
        $scope.$emit('updateTeacherEmailEvent', teacherEmail);
    };

});

edjectiveApp.controller('LookupCtrl', function ($scope, $http) {

    $scope.objectives = {'data': [{'text': 'class1', 'objectives': ['obj1', 'obj2']},
                                  {'text': 'class2', 'objectives': ['obj2a', 'obj2b']}]};

    $scope.$on('handleTeacherEmailBroadcast', function(event, args) {
        $scope.notice = {'text': 'loading ' + args + '...'};

        $http.get('http://127.0.0.1:8000/teachers/api/teacher_class/?format=json&teacher__email=' + args).success(function(data) {
            if (data.meta.total_count == 0) {
                $scope.notice = {'text': 'Invalid teacher e-mail address!'};
            }
            else {
                $scope.notice = {'text': ''};
                $scope.classes = data.objects;
            }
        });
    });
});

