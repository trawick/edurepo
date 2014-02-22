var edjectiveApp = angular.module('edjectiveApp', ['ngRoute']);

edjectiveApp.config(function($routeProvider) {
    $routeProvider

    .when('/', {
        templateUrl: 'pages/front.html',
        controller: 'FrontCtrl'
    })

    .when('/keyIdeas', {
        templateUrl: 'pages/keyIdeas.html',
        controller: 'FrontCtrl'
    })

    .when('/forParents', {
        templateUrl: 'pages/currentObjectives.html',
        controller: 'LookupCtrl'
    })

    .when('/forTeachers', {
        templateUrl: 'pages/forTeachers.html',
        controller: 'ForTeachersCtrl'
    })

    .when('/forAuthors', {
        templateUrl: 'pages/forAuthors.html',
        controller: 'FrontCtrl'
    })

    .when('/forVendors', {
        templateUrl: 'pages/forVendors.html',
        controller: 'FrontCtrl'
    })

    .when('/QandA', {
        templateUrl: 'pages/qanda.html',
        controller: 'FrontCtrl'
    })

    .when('/forNerds', {
        templateUrl: 'pages/forNerds.html',
        controller: 'FrontCtrl'
    })

    .otherwise({redirectTo: '/', controller: 'LookupCtrl'});
})

edjectiveApp.run(function($rootScope) {
    $rootScope.$on('updateTeacherEmailEvent', function(event, args) {
        $rootScope.$broadcast('handleTeacherEmailBroadcast', args);
    });
});

edjectiveApp.controller('FrontCtrl', function ($scope) {
    // nothing for now
});

edjectiveApp.controller('ForTeachersCtrl', function ($scope) {
    // nothing for now
});

edjectiveApp.controller('GetTeacherEmailCtrl', function ($scope) {

    $scope.update = function(teacherEmail) {
        $scope.$emit('updateTeacherEmailEvent', teacherEmail);
    };

});

edjectiveApp.controller('LookupCtrl', function ($scope, $http, $filter) {

    $scope.objectives = {'data': []};
    $scope.teacher_email = '';

    function setBaseURL(u) {
        $scope.baseurl = u;
        $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';
        $scope.res_baseurl = $scope.baseurl + 'resources/api/resource/';
    }

    function annotate_objective($http, data, obj) {
        return function(data) {
            obj.objective = data.id + ' ' + data.formal_description;
            obj.resources = [];
            $http.get(lookup_resources_url(data.id)).success(function(data) {
                obj.resources = data.objects;
            });
        };
    }

    function lookup_objective_url(obj) {
        return $scope.lo_baseurl + obj + '/';
    }

    // /resources/api/resource/?format=json&resource_objective=MG4-FACTMULT
    function lookup_resources_url(obj) {
        return $scope.res_baseurl + '?resource_objective=' + obj;
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
                    $http.get(lookup_objective_url(data.objects[i].objective)).success(annotate_objective($http, data, newobj.objectives[newobj.objectives.length - 1]));
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

        $http.get("resources/config.json").success(function(data) {

            setBaseURL(data.base_api_url);

            $http.get(lookup_teacher_classes_url(args)).success(function(data) {
                if (data.meta.total_count == 0) {
                    $scope.notice = {'text': 'Invalid teacher e-mail address!'};
                }
                else {
                    $scope.notice = {'text': "Select one or more of this teacher's classes:"};
                    $scope.classes = data.objects;
                }
            });

        });
    });
});
