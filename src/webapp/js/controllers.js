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
    $scope.baseurl = 'http://127.0.0.1:8000/';
    $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';

    function annotate_objective(data, obj) {
        return function(data) {
            obj.objective = data.id + ' ' + data.formal_description;
        };
    }

    function lookup_objective_url(obj) {
        return $scope.lo_baseurl + obj + '/';
    }

    function lookup_current_objectives_url(teacher_email, start_date, stop_date, class_name) {
        return $scope.baseurl + 'teachers/api/entry/?teacher__email=' + teacher_email + '&date__lte=' + stop_date + '&date__gte=' + start_date + '&teacher_class__name=' + class_name;
    }

    function lookup_teacher_classes_url(teacher_email) {
        return $scope.baseurl + 'teachers/api/teacher_class/?teacher__email=' + teacher_email;
    }

    $scope.classSelection = function(cl) {
        // Key data is cl.name and cl.isSelected
        if (cl.isSelected) {
            var curdate = new Date();
            var curdatestr = $filter('date')(curdate, 'yyyy-MM-dd');
            var weekago = new Date();
            weekago.setDate(weekago.getDate() - 7);
            var weekagostr = $filter('date')(weekago, 'yyyy-MM-dd');
            $http.get(lookup_current_objectives_url($scope.teacher_email, weekagostr, curdatestr, cl.name)).success(function(data) {
                var newobj = {'text': cl.name, 'objectives': []};
                for (var i = 0; i < data.meta.total_count; i++) {
                    newobj.objectives.push({'date': data.objects[i].date, 'objective': data.objects[i].objective});
                    $http.get(lookup_objective_url(data.objects[i].objective)).success(annotate_objective(data, newobj.objectives[newobj.objectives.length - 1]));
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

        $http.get(lookup_teacher_classes_url(args)).success(function(data) {
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
