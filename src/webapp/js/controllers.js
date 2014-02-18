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

edjectiveApp.controller('LookupCtrl', function ($scope, $http, $filter) {

    $scope.objectives = {'data': []};

    $scope.teacher_email = '';

    $scope.classSelection = function(cl) {
        // Key data is cl.name and cl.isSelected
        if (cl.isSelected) {
            var curdate = new Date();
            var curdatestr = $filter('date')(curdate, 'yyyy-MM-dd');
            var weekago = new Date();
            weekago.setDate(weekago.getDate() - 7);
            var weekagostr = $filter('date')(weekago, 'yyyy-MM-dd');
            $http.get('http://127.0.0.1:8000/teachers/api/entry/?format=json&teacher__email=' + $scope.teacher_email + '&date__lte=' + curdatestr + '&date__gte=' + weekagostr + '&teacher_class__name=' + cl.name).success(function(data) {
                var newobj = {'text': cl.name, 'objectives': []};
                for (var i = 0; i < data.meta.total_count; i++) {
                    newobj.objectives.push({'date': data.objects[i].date, 'objective': data.objects[i].objective});
                }
                $scope.objectives['data'].push(newobj);
            });
        }
        else {
            for (var i = 0; i < $scope.objectives.data.length; i++) {
                if ($scope.objectives.data[i].text == cl.name) {
                    $scope.objectives.data.splice(i, 1);
                    break;
                }
            }
        }
    };

    $scope.$on('handleTeacherEmailBroadcast', function(event, args) {
        $scope.teacher_email = args;
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
