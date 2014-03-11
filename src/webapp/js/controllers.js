var edjectiveApp = angular.module('edjectiveApp', ['ngRoute']);

edjectiveApp.factory('CurrentObjectives', function() {
    var c_o = null;
    return {
        get: function () {
            return c_o;
        },
        set: function (new_c_o) {
            c_o = new_c_o;
        }
    };
});

edjectiveApp.config(function($routeProvider) {
    $routeProvider

    .when('/', {
        templateUrl: 'pages/front.html',
        controller: 'FrontCtrl'
    })

    .when('/browse/:objective', {
        templateUrl: 'pages/browseObjective.html',
        controller: 'BrowseObjectiveCtrl'
    })

    .when('/browse', {
        templateUrl: 'pages/browse.html',
        controller: 'BrowseCtrl'
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
        controller: 'CourseLookupCtrl'
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

edjectiveApp.controller('BrowseObjectiveCtrl', function ($scope, $http, $routeParams, CurrentObjectives) {
    $scope.baseurl = null;
    $scope.objective_name = $routeParams.objective;
    $scope.objective = null;
    $scope.all_objectives = CurrentObjectives.get();
    $scope.previous_objective = null;
    $scope.next_objective = null;
    $scope.resources = null;

    function setBaseURL(u) {
        $scope.baseurl = u;
        $scope.coursecat_baseurl = $scope.baseurl + 'repo/api/coursecategory/';
        $scope.course_baseurl = $scope.baseurl + 'repo/api/course/';
        $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';
        $scope.res_baseurl = $scope.baseurl + 'resources/api/resource/';
        $scope.reference_baseurl = $scope.baseurl + 'repo/api/referencetext/';
        $scope.multiplechoice_baseurl = $scope.baseurl + 'repo/api/multiplechoiceitem/';
        $scope.res_create_form = $scope.baseurl + 'resources/create/';
    }

    function lookup_resources_url(obj) {
        return $scope.res_baseurl + '?objective__id=' + obj;
    }

    $scope.submitResource = function(objective_id) {
        window.location.replace($scope.res_create_form + '?objective=' + objective_id);
    };

    $scope.calcPrevNext = function() {
        for (var i = 0; i < $scope.all_objectives.length; i++) {
            this_objective = $scope.all_objectives[i];
            if (this_objective.id == $scope.objective.id) {
                if (i > 0) {
                    $scope.previous_objective = $scope.all_objectives[i - 1];
                }
                if (i + 1 < $scope.all_objectives.length) {
                    $scope.next_objective = $scope.all_objectives[i + 1];
                }
                break;
            }
        }
    };

    // Kick everything off once we retrieve the API configuration.
    $http.get("resources/config.json").success(function(data) {
        setBaseURL(data.base_api_url);

        $http.get($scope.lo_baseurl + '?id=' + $scope.objective_name).success(function(data) {
            $scope.objective = data.objects[0];

            if ($scope.all_objectives) {
                $scope.calcPrevNext();
            }
            else {
                // Load all objectives since we somehow got here without it.
                $http.get($scope.lo_baseurl + '?course__id=' + $scope.objective.course_id).success(function(data) {
                    $scope.all_objectives = data.objects;
                    CurrentObjectives.set(data.objects);
                    $scope.calcPrevNext();
                });
            }
        });

        $http.get(lookup_resources_url($scope.objective_name)).success(function(data) {
            $scope.resources = data.objects;
        });
    });

});

edjectiveApp.controller('BrowseCtrl', function ($scope, $http, CurrentObjectives) {
    $scope.baseurl = '';
    $scope.categories = null;
    $scope.selectedCategory = null;
    $scope.courses = null;
    $scope.selectedCourse = null;
    $scope.objectives = null;
    $scope.serverUnreachable = null;

    function setBaseURL(u) {
        $scope.baseurl = u;
        $scope.coursecat_baseurl = $scope.baseurl + 'repo/api/coursecategory/';
        $scope.course_baseurl = $scope.baseurl + 'repo/api/course/';
        $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';
        $scope.res_baseurl = $scope.baseurl + 'resources/api/resource/';
        $scope.reference_baseurl = $scope.baseurl + 'repo/api/referencetext/';
        $scope.multiplechoice_baseurl = $scope.baseurl + 'repo/api/multiplechoiceitem/';
    }

    $scope.updateSelectedCategory = function() {
        $scope.courses = null;
        $scope.objectives = null;
        $http.get($scope.course_baseurl + '?cat__id=' + $scope.selectedCategory.id).success(function(data) {
            $scope.courses = data.objects;
        });
    };

    $scope.updateSelectedCourse = function() {
        $http.get($scope.lo_baseurl + '?course__id=' + $scope.selectedCourse.id).success(function(data) {
            $scope.objectives = data.objects;
            CurrentObjectives.set(data.objects);
        });
    };

    // Kick everything off once we retrieve the API configuration.
    $http.get("resources/config.json").success(function(data) {
        setBaseURL(data.base_api_url);

        $http.get($scope.coursecat_baseurl).success(function(data) {
            $scope.categories = data.objects;
        }).error(function(data) {
            $scope.serverUnreachable = "The server cannot be reached.";
        });
    }).error(function(data) {
        $scope.serverUnreachable = "The server cannot be reached.";
    });

});

edjectiveApp.controller('CourseLookupCtrl', function ($scope, $http) {
    $scope.courseId = '';
    $scope.objectives = [];
    $scope.baseurl = '';
    $scope.lo_baseurl = '';
    $scope.res_baseurl = '';

    function setBaseURL(u) {
        $scope.baseurl = u;
        $scope.course_baseurl = $scope.baseurl + 'repo/api/course/';
        $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';
        $scope.res_baseurl = $scope.baseurl + 'resources/api/resource/';
        $scope.reference_baseurl = $scope.baseurl + 'repo/api/referencetext/';
        $scope.multiplechoice_baseurl = $scope.baseurl + 'repo/api/multiplechoiceitem/';
    }

    $http.get("resources/config.json").success(function(data) {
        setBaseURL(data.base_api_url);
    });

    $scope.update = function(courseId) {
        if ($scope.baseurl != '') {
            updateCourse(courseId);
        }
    };

    function lookup_course(courseId) {
        return $scope.course_baseurl + courseId + '/';
    }

    function lookup_objectives_by_course(course_id) {
        return $scope.lo_baseurl + '?course=' + course_id;
    }

    function lookup_glossary_items_by_objective(obj) {
        return $scope.baseurl + 'repo/api/glossary_item/?learning_objective__id=' + obj;
    }

    function lookup_icans_by_objective(obj) {
        return $scope.baseurl + 'repo/api/ican/?learning_objective__id=' + obj;
    }

    function lookup_referencetext_by_objective(obj) {
        return $scope.reference_baseurl + '?learning_objective=' + obj;
    }

    function lookup_multiple_choice_items_by_objective(obj) {
        return $scope.multiplechoice_baseurl + '?learning_objective__id=' + obj;
    }

    function lookup_true_false_items_by_objective(obj) {
        return $scope.baseurl + 'repo/api/true_false_item/?learning_objective__id=' + obj;
    }

    function lookup_resources_url(obj) {
        return $scope.res_baseurl + '?objective=' + obj;
    }

    function annotate_objective($http, obj) {
        obj.objective = obj.id + ' ' + obj.description;
        obj.resources = [];
        obj.glossitems = [];
        obj.icans = [];
        $http.get(lookup_icans_by_objective(obj.id)).success(function(data) {
            obj.icans = data.objects;
        });
        $http.get(lookup_referencetext_by_objective(obj.id)).success(function(data) {
            obj.referencetext = data.objects[0];
        });
        $http.get(lookup_resources_url(obj.id)).success(function(data) {
            obj.resources = data.objects;
        });
        $http.get(lookup_glossary_items_by_objective(obj.id)).success(function(data) {
            obj.glossitems = data.objects;
        });
        $http.get(lookup_true_false_items_by_objective(obj.id)).success(function(data) {
            obj.tfitems = data.objects;
        });
        $http.get(lookup_multiple_choice_items_by_objective(obj.id)).success(function(data) {
            obj.mcitems = data.objects;
        });
    }

    function updateCourse(courseId) {
        $scope.courseId = courseId;
        $scope.course = null;
        $scope.courseLookupError = '';

        $http.get(lookup_course(courseId)).success(function (data) {
            $scope.course = data;
        });

        $http.get(lookup_objectives_by_course(courseId)).success(function (data) {
            if (data.meta.total_count == 0) {
                $scope.courseLookupError = 'The course id is not valid.';
            }
            else {
                $scope.objectives = data.objects;
                for (var i = 0; i < data.meta.total_count; i++) {
                    if (data.objects[i]) { // may have hit limit
                        annotate_objective($http, data.objects[i]);
                    }
                }
            }
        }).error(function () {
            $scope.courseLookupError = 'The server could not be contacted.';
        });
    }
});

edjectiveApp.controller('LookupCtrl', function ($scope, $http, $filter) {

    $scope.objectives = {'data': []};
    $scope.teacher_email = '';

    function setBaseURL(u) {
        $scope.baseurl = u;
        $scope.lo_baseurl = $scope.baseurl + 'repo/api/learningobjective/';
        $scope.res_baseurl = $scope.baseurl + 'resources/api/resource/';
        $scope.reference_baseurl = $scope.baseurl + 'repo/api/referencetext/';
        $scope.multiplechoice_baseurl = $scope.baseurl + 'repo/api/multiplechoiceitem/';
    }

    function annotate_objective($http, data, obj) {
        return function(data) {
            obj.objective = data.id + ' ' + data.description;
            obj.resources = [];
            obj.glossitems = [];
            obj.icans = [];
            $http.get(lookup_icans_by_objective(data.id)).success(function(data) {
                obj.icans = data.objects;
            });
            $http.get(lookup_referencetext_by_objective(data.id)).success(function(data) {
                obj.referencetext = data.objects[0];
            });
            $http.get(lookup_resources_url(data.id)).success(function(data) {
                obj.resources = data.objects;
            });
            $http.get(lookup_glossary_items_by_objective(data.id)).success(function(data) {
                obj.glossitems = data.objects;
            });
            $http.get(lookup_true_false_items_by_objective(data.id)).success(function(data) {
                obj.tfitems = data.objects;
            });
            $http.get(lookup_multiple_choice_items_by_objective(data.id)).success(function(data) {
                obj.mcitems = data.objects;
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

    function lookup_glossary_items_by_objective(obj) {
        return $scope.baseurl + 'repo/api/glossary_item/?learning_objective__id=' + obj;
    }

    function lookup_icans_by_objective(obj) {
        return $scope.baseurl + 'repo/api/ican/?learning_objective__id=' + obj;
    }

    function lookup_referencetext_by_objective(obj) {
        return $scope.reference_baseurl + '?learning_objective=' + obj;
    }

    function lookup_multiple_choice_items_by_objective(obj) {
        return $scope.multiplechoice_baseurl + '?learning_objective__id=' + obj;
    }

    function lookup_true_false_items_by_objective(obj) {
        return $scope.baseurl + 'repo/api/true_false_item/?learning_objective__id=' + obj;
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
                    newobj.objectives.push({'date': data.objects[i].date, 'objective': data.objects[i].objective,
                                            'comments': data.objects[i].comments});
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
        $scope.notice = {'text': 'Loading ' + args + '...'};

        $http.get("resources/config.json").success(function(data) {

            setBaseURL(data.base_api_url);

            $http.get(lookup_teacher_classes_url(args)).success(function(data) {
                if (data.meta.total_count == 0) {
                    $scope.notice = {'text': 'The teacher e-mail address is invalid.'};
                }
                else {
                    $scope.notice = {'text': "Select one or more of this teacher's classes:"};
                    $scope.classes = data.objects;
                }
            }).error(function () {
                $scope.notice.text = 'The server could not be contacted.';
            });;

        }).error(function () {
            $scope.notice.text = 'The server could not be contacted.';
        });
    });
});
