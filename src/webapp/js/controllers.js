var edjectiveApp = angular.module('edjectiveApp', ['ngRoute']);

var edjectiveAppUrls = {};
edjectiveAppUrls['setBase'] = function(base) {
    edjectiveAppUrls['base'] = base;
    edjectiveAppUrls['coursecat_baseurl'] = base + 'repo/api/coursecategory/';
    edjectiveAppUrls['course_baseurl'] = base + 'repo/api/course/';
    edjectiveAppUrls['lo_baseurl'] = base + 'repo/api/learningobjective/';
    edjectiveAppUrls['res_baseurl'] = base + 'resources/api/resource/';
    edjectiveAppUrls['reference_baseurl'] = base + 'repo/api/referencetext/';
    edjectiveAppUrls['multiplechoice_baseurl'] = base + 'repo/api/multiplechoiceitem/';
    edjectiveAppUrls['comments_baseurl'] = base + 'resources/api/resourcesubmission/';
};
edjectiveAppUrls['getCategories'] = function() {
    return edjectiveAppUrls.coursecat_baseurl;
};
edjectiveAppUrls['getCourse'] = function(course_id) {
    return edjectiveAppUrls.course_baseurl + course_id + '/';
};
edjectiveAppUrls['getObjective'] = function(objective_id) {
    return edjectiveAppUrls.lo_baseurl + objective_id + '/';
};
edjectiveAppUrls['getObjectiveFromName'] = function(objective_name) {
    return edjectiveAppUrls.lo_baseurl + '?id=' + objective_name;
};
edjectiveAppUrls['getCoursesFromCategory'] = function(category_id) {
    return edjectiveAppUrls.course_baseurl + '?cat__id=' + category_id;
};
edjectiveAppUrls['getObjectivesFromCourse'] = function(course_id) {
    return edjectiveAppUrls.lo_baseurl + '?course__id=' + course_id;
};
edjectiveAppUrls['getGlossaryItemsFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.base + 'repo/api/glossary_item/?learning_objective__id=' + objective_id;
};
edjectiveAppUrls['getIcansFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.base + 'repo/api/ican/?learning_objective__id=' + objective_id;
};
edjectiveAppUrls['getReferenceTextFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.reference_baseurl + '?learning_objective=' + objective_id;
};
edjectiveAppUrls['getResourcesFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.res_baseurl + '?objective__id=' + objective_id;
};
edjectiveAppUrls['getMultipleChoiceItemsFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.multiplechoice_baseurl + '?learning_objective__id=' + objective_id;
};
edjectiveAppUrls['getTrueFalseItemsFromObjective'] = function(objective_id) {
    return edjectiveAppUrls.base + 'repo/api/true_false_item/?learning_objective__id=' + objective_id;
};
edjectiveAppUrls['getClassesFromTeacher'] = function(teacher_email) {
    return edjectiveAppUrls.base + 'teachers/api/teacher_class/?teacher__email=' + teacher_email;
};
edjectiveAppUrls['getObjectivesFromTeacherClass'] = function(teacher_email, start_date, stop_date, class_name) {
    return edjectiveAppUrls.base + 'teachers/api/entry/?teacher__email=' + teacher_email + '&date__lte=' + stop_date + '&date__gte=' + start_date + '&teacher_class__name=' + class_name;
};
edjectiveAppUrls['getCommentsFromResource'] = function(resource_id) {
    return edjectiveAppUrls.comments_baseurl + '?resource=' + resource_id;
};
edjectiveAppUrls['getResourceEntryForm'] = function(objective_id) {
    return edjectiveAppUrls.base + 'resources/create/' + '?objective=' + objective_id;
};
edjectiveAppUrls['getResourceCommentForm'] = function(resource_id) {
    return edjectiveAppUrls.base + 'resources/' + resource_id + '/comment';
};
edjectiveAppUrls['getUserInterface'] = function() {
    return edjectiveAppUrls.base;
};

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

edjectiveApp.factory('Flashcards', function () {
    var flashcards = null;
    return {
        get: function () {
            return flashcards;
        },
        set: function (new_flashcards) {
            flashcards = new_flashcards;
        }
    };
});

edjectiveApp.config(function($routeProvider) {
    $routeProvider

    .when('/', {
        templateUrl: 'pages/front.html',
        controller: 'FrontCtrl'
    })

    .when('/myEdjectives', {
        templateUrl: 'pages/myEdjectives.html',
        controller: 'MyEdjectivesCtrl'
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

    .when('/flashcards', {
        templateUrl: 'pages/flashcards.html',
        controller: 'FlashcardCtrl'
    })

    .otherwise({redirectTo: '/', controller: 'LookupCtrl'});
});

edjectiveApp.run(function($rootScope) {
    $rootScope.$on('updateTeacherEmailEvent', function(event, args) {
        $rootScope.$broadcast('handleTeacherEmailBroadcast', args);
    });
});

edjectiveApp.controller('FrontCtrl', function ($scope) {
    // nothing for now
});

edjectiveApp.controller('MyEdjectivesCtrl', function ($scope, $http, $filter, $location, Flashcards) {
    $scope.studentData = [];
    $scope.flashcards = Flashcards;

    $scope.glossaryFlashcards = function (obj) {
        var flashcards = [];
        for (var i = 0; i < obj.glossitems.length; i++) {
            var item = obj.glossitems[i];
            var card = [item.term, item.definition];
            flashcards.push(card);
        }
        $scope.flashcards.set(flashcards);
        $location.path("flashcards");
    };

    $scope.enableAddClassWidget = function () {
        for (var i = 0; i < $scope.studentData.length; i++) {
            $scope.studentData[i].enableAdd = false;
        }
        this.student.enableAdd = true;
    };

    $scope.disableAddClassWidget = function () {
        this.student.enableAdd = false;
        this.student.teacherOfNewClass = '';
        this.student.addClassTeacherClasses = [];
    };

    $scope.addClassTeacherLookup = function () {
        var student = this.student;
        var studentName = this.student.name;
        var teacher = $("#new-class-" + studentName).val();
        if (teacher == '') {
            // XXX use an error message field instead
            alert('Please provide a teacher e-mail address.');
        }
        this.student.teacherOfNewClass = teacher;
        var url = edjectiveAppUrls['getClassesFromTeacher'](this.student.teacherOfNewClass);
        $http.get(url).success(function(data) {
            if (data.meta.total_count == 0) {
                // XXX use an error message field instead
                alert('No classes for teacher ' + teacher);
                $scope.addClassNotice = 'The teacher e-mail address is invalid.';
            }
            else {
                student.addClassTeacherClasses = [];
                for (var i = 0; i < data.objects.length; i++) {
                    student.addClassTeacherClasses.push(data.objects[i].name);
                }
            }
        });
    };

    $scope.addClass = function () {
        var classIndex = $("#addClassSelectedClass-" + this.student.name).val();

        for (var i = 0; i < $scope.studentData.length; i++) {
            if ($scope.studentData[i].name == this.student.name) {
                // XXX don't add same class again!
                $scope.studentData[i].classes.push({'teacherEmail': this.student.teacherOfNewClass,
                                                    'className': this.student.addClassTeacherClasses[classIndex]});
                $scope.saveConfig();
                // XXX load objectives for the new class so that user doesn't have to refresh
                break;
            }
        }
        this.student.teacherOfNewClass = '';
        this.student.addClassTeacherClasses = [];
        this.student.enableAdd = false;
    };

    $scope.removeClass = function () {
        var student = this.$parent.student;
        var studentClasses = student.classes;
        var classToRemove = this.class;

        for (var i = 0; i < studentClasses.length; i++) {
            if (studentClasses[i].className == classToRemove.className) {
                studentClasses.splice(i, 1);
                $scope.saveConfig();
                break;
            }
        }
    };

    $scope.saveConfig = function () {
        // XXX Try saving/restoring JSON.
        localStorage['MyEdjectives.numStudents'] = $scope.studentData.length;
        for (var i = 0; i < $scope.studentData.length; i++) {
            localStorage['MyEdjectives.' + i + '.name'] = $scope.studentData[i].name;
            localStorage['MyEdjectives.' + i + '.numClasses'] = $scope.studentData[i].classes.length;
            for (var j = 0; j < $scope.studentData[i].classes.length; j++) {
                localStorage['MyEdjectives.' + i + '.' + j + '.teacherEmail'] = $scope.studentData[i].classes[j].teacherEmail;
                localStorage['MyEdjectives.' + i + '.' + j + '.className'] = $scope.studentData[i].classes[j].className;
            }
        }
    };

    $scope.loadConfig = function () {
        $scope.studentData = [];
        var numStudents = localStorage['MyEdjectives.numStudents'];
        for (var i = 0; i < numStudents; i++) {
            var studentData = {
                'classes': []
            };
            studentData['name'] = localStorage['MyEdjectives.' + i + '.name'];
            var numClasses = localStorage['MyEdjectives.' + i + '.numClasses'];
            for (var j = 0; j < numClasses; j++) {
                var classData = {};
                classData['teacherEmail'] = localStorage['MyEdjectives.' + i + '.' + j + '.teacherEmail'];
                classData['className'] = localStorage['MyEdjectives.' + i + '.' + j + '.className'];
                studentData['classes'].push(classData);
            }
            $scope.studentData.push(studentData);
        }
    };

    function receiveClassObjectivesFunction(studentNum, classNum) {
        return function(data) {
            $scope.studentData[studentNum].classes[classNum].objectives = [];
            var objectives = $scope.studentData[studentNum].classes[classNum].objectives;

            for (var i = 0; i < data.objects.length; i++) {
                var objectiveDate = data.objects[i].date;
                var objectiveName = data.objects[i].objective;

                var objectiveData = {};
                $http.get(edjectiveAppUrls.getGlossaryItemsFromObjective(objectiveName)).success(function(data) {
                    objectiveData.glossitems = data.objects;
                });
                $http.get(edjectiveAppUrls.getTrueFalseItemsFromObjective(data.id)).success(function(data) {
                    objectiveData.tfitems = data.objects;
                });
                objectives.push({'name': objectiveName,
                                 'date': objectiveDate,
                                 'data': objectiveData});
            }
        };
    }

    $scope.loadData = function () {
        for (var i = 0; i < $scope.studentData.length; i++) {
            var studentData = $scope.studentData[i];
            for (var j = 0; j < studentData.classes.length; j++) {
                var classData = studentData.classes[j];

                var curdate = new Date();
                var curdatestr = $filter('date')(curdate, 'yyyy-MM-dd');
                var weekago = new Date();
                weekago.setDate(weekago.getDate() - 7);
                var weekagostr = $filter('date')(weekago, 'yyyy-MM-dd');

                var url = edjectiveAppUrls['getObjectivesFromTeacherClass'](classData['teacherEmail'],
                    weekagostr, curdatestr,
                    classData['className']);

                $http.get(url).success(receiveClassObjectivesFunction(i, j));
            }
        }
    };

    $scope.addStudent = function() {
        // XXX Make sure student name is unique!
        var newName = $("#new-student-name").val();
        $scope.studentData.push({'name': newName,
                                 'classes': []});
        $scope.saveConfig();
    };

    $scope.removeStudent = function() {
        for (var i = 0; i < $scope.studentData.length; i++) {
            if ($scope.studentData[i].name == this.student.name) {
                $scope.studentData.splice(i, 1);
                $scope.saveConfig();
                break;
            }
        }
    };

    $scope.loadConfig();

    $http.get("resources/config.json").success(function(data) {
        // XXX Should we block out the UI for adding students until this is complete?
        edjectiveAppUrls.setBase(data['base_api_url']);

        $scope.loadData();
    });
    // XXX error path: update an error message field
});

edjectiveApp.controller('ForTeachersCtrl', function ($scope, $http) {
    // Kick everything off once we retrieve the API configuration.
    $http.get("resources/config.json").success(function(data) {
        edjectiveAppUrls.setBase(data['base_api_url']);
        $scope.webui = edjectiveAppUrls.getUserInterface();
    });
});

edjectiveApp.controller('BrowseObjectiveCtrl', function ($scope, $http, $routeParams, $sce, CurrentObjectives) {
    $scope.objective_name = $routeParams.objective;
    $scope.objective = null;
    $scope.all_objectives = CurrentObjectives.get();
    $scope.previous_objective = null;
    $scope.next_objective = null;
    $scope.resources = null;
    $scope.no_resources_msg = ''; // No educational resources have been submitted.

    $scope.submitResource = function(objective_id) {
        window.open(edjectiveAppUrls.getResourceEntryForm(objective_id),
                    "Resource for " + objective_id);
    };

    $scope.commentOnResource = function(resource_id) {
        window.open(edjectiveAppUrls.getResourceCommentForm(resource_id),
                    "Comment on resource");
    };

    $scope.toTrusted = function(html) {
        return $sce.trustAsHtml(html);
    };

    $scope.calcPrevNext = function() {
        for (var i = 0; i < $scope.all_objectives.length; i++) {
            var this_objective = $scope.all_objectives[i];
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
        edjectiveAppUrls.setBase(data['base_api_url']);

        $http.get(edjectiveAppUrls.getObjectiveFromName($scope.objective_name)).success(function(data) {
            $scope.objective = data.objects[0];

            if ($scope.all_objectives) {
                $scope.calcPrevNext();
            }
            else {
                // Load all objectives since we somehow got here without it.
                $http.get(edjectiveAppUrls.getObjectivesFromCourse($scope.objective.course_id)).success(function(data) {
                    $scope.all_objectives = data.objects;
                    CurrentObjectives.set(data.objects);
                    $scope.calcPrevNext();
                });
            }
        });

        function annotate_resource(resource) {
            return function(data) {
                resource.upvotes = [];
                resource.flags = [];
                for (var i = 0; i < data.objects.length; i++) {
                    if (data.objects[i].type == "f") {
                        resource.flags.push(data.objects[i]);
                    }
                    else {
                        resource.upvotes.push(data.objects[i]);
                    }
                }
            }
        }

        $http.get(edjectiveAppUrls.getResourcesFromObjective($scope.objective_name)).success(function(data) {
            $scope.resources = data.objects;
            var is_secure = /^https:/.exec(window.location);
            var youtube_scheme = is_secure ? "https" : "http";
            var regex = /youtube.com.*v=(.*)/;
            if ($scope.resources.length == 0) {
                $scope.no_resources_msg = 'No educational resources have been submitted.';
            }
            for (var i = 0; i < $scope.resources.length; i++) {
                var match = regex.exec($scope.resources[i].url);
                if (match) {
                    $scope.resources[i].embed =
                        '<iframe title="YouTube Video" type="text/html" src="'
                        + youtube_scheme + '://youtube.com/embed/' + match[1] + '" />';
                }

                if ($scope.resources[i].status != 'V') {
                    $scope.resources[i].warning = 'This resource may not be accessible.';
                }
                else if ($scope.resources[i].inappropriate_flags != 0) {
                    $scope.resources[i].warning = 'This resource has been flagged as inappropriate.';
                }
                else if ($scope.resources[i].content_type != 'text/html') {
                    $scope.resources[i].warning = 'This resource might not be viewable in your web browser.';
                }
                else {
                    $scope.resources[i].warning = '';
                }
                $http.get(edjectiveAppUrls.getCommentsFromResource($scope.resources[i].id)).success(annotate_resource($scope.resources[i]));
            }
        });
    });

});

edjectiveApp.controller('BrowseCtrl', function ($scope, $http, CurrentObjectives) {
    $scope.categories = null;
    $scope.selectedCategory = null;
    $scope.courses = null;
    $scope.selectedCourse = null;
    $scope.objectives = null;
    $scope.serverUnreachable = null;

    $scope.updateSelectedCategory = function() {
        $scope.courses = null;
        $scope.objectives = null;
        $http.get(edjectiveAppUrls.getCoursesFromCategory($scope.selectedCategory.id)).success(function(data) {
            $scope.courses = data.objects;
        });
    };

    $scope.updateSelectedCourse = function() {
        if ($scope.selectedCourse == null) {
            return;
        }
        $http.get(edjectiveAppUrls.getObjectivesFromCourse($scope.selectedCourse.id)).success(function(data) {
            $scope.objectives = data.objects;
            CurrentObjectives.set(data.objects);
        });
    };

    // Kick everything off once we retrieve the API configuration.
    $http.get("resources/config.json").success(function(data) {
        edjectiveAppUrls.setBase(data['base_api_url']);

        $http.get(edjectiveAppUrls.getCategories()).success(function(data) {
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
    $scope.initialized = 0;

    $http.get("resources/config.json").success(function(data) {
        edjectiveAppUrls.setBase(data['base_api_url']);
        $scope.initialized = 1;
    });

    $scope.update = function(courseId) {
        if ($scope.initialized != 0) {
            updateCourse(courseId);
        }
    };

    function annotate_objective($http, obj) {
        obj.objective = obj.id + ' ' + obj.description;
        obj.resources = [];
        obj.glossitems = [];
        obj.icans = [];
        $http.get(edjectiveAppUrls.getIcansFromObjective(obj.id)).success(function(data) {
            obj.icans = data.objects;
        });
        $http.get(edjectiveAppUrls.getReferenceTextFromObjective(obj.id)).success(function(data) {
            obj.referencetext = data.objects[0];
        });
        $http.get(edjectiveAppUrls.getResourcesFromObjective(obj.id)).success(function(data) {
            obj.resources = data.objects;
        });
        $http.get(edjectiveAppUrls.getGlossaryItemsFromObjective(obj.id)).success(function(data) {
            obj.glossitems = data.objects;
        });
        $http.get(edjectiveAppUrls.getTrueFalseItemsFromObjective(obj.id)).success(function(data) {
            obj.tfitems = data.objects;
        });
        $http.get(edjectiveAppUrls.getMultipleChoiceItemsFromObjective(obj.id)).success(function(data) {
            obj.mcitems = data.objects;
        });
    }

    function updateCourse(courseId) {
        $scope.courseId = courseId;
        $scope.course = null;
        $scope.courseLookupError = '';

        $http.get(edjectiveAppUrls.getCourse(courseId)).success(function (data) {
            $scope.course = data;
        });

        $http.get(edjectiveAppUrls.getObjectivesFromCourse(courseId)).success(function (data) {
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

edjectiveApp.controller('GetTeacherEmailCtrl', function ($scope) {
    $scope.teacherEmail = 'ms.teacher@example.edu';
    $scope.update = function(teacherEmail) {
        $scope.$emit('updateTeacherEmailEvent', teacherEmail);
    };

});

edjectiveApp.controller('LookupCtrl', function ($scope, $http, $filter, $location, Flashcards) {

    $scope.objectives = {'data': []};
    $scope.teacher_email = '';
    $scope.flashcards = Flashcards;
    $scope.trueFalseFlashcards = function (obj) {
        // Flashcards are just an array of arrays, where the inner arrays
        // are the front side of the flash card in the first element and
        // the back side in the second element.
        var flashcards = [];
        for (var i = 0; i < obj.tfitems.length; i++) {
            var card = [obj.tfitems[i].statement, obj.tfitems[i].answer.toString()];
            flashcards.push(card);
        }
        $scope.flashcards.set(flashcards);
        $location.path("flashcards");
    };

    $scope.glossaryFlashcards = function (obj) {
        var flashcards = [];
        for (var i = 0; i < obj.glossitems.length; i++) {
            var item = obj.glossitems[i];
            var card = [item.term, item.definition];
            flashcards.push(card);
        }
        $scope.flashcards.set(flashcards);
        $location.path("flashcards");
    };

    $scope.multipleChoiceFlashcards = function (obj) {
        var flashcards = [];
        for (var i = 0; i < obj.mcitems.length; i++) {
            var item = obj.mcitems[i];
            var ans;
            if (item.ans == 1) {
                ans = item.choice1;
            }
            else if (item.ans == 2) {
                ans = item.choice2;
            }
            else if (item.ans == 3) {
                ans = item.choice3;
            }
            else if (item.ans == 4) {
                ans = item.choice4;
            }
            else if (item.ans == 5) {
                ans = item.choice5;
            }
            var card = [item.question, ans];
            flashcards.push(card);
        }
        $scope.flashcards.set(flashcards);
        $location.path("flashcards");
    };

    function annotate_objective($http, data, obj) {
        return function(data) {
            obj.objective = data.id + ' ' + data.description;
            obj.resources = [];
            obj.glossitems = [];
            obj.icans = [];
            $http.get(edjectiveAppUrls.getIcansFromObjective(data.id)).success(function(data) {
                obj.icans = data.objects;
            });
            $http.get(edjectiveAppUrls.getReferenceTextFromObjective(data.id)).success(function(data) {
                obj.referencetext = data.objects[0];
            });
            $http.get(edjectiveAppUrls.getResourcesFromObjective(data.id)).success(function(data) {
                obj.resources = data.objects;
            });
            $http.get(edjectiveAppUrls.getGlossaryItemsFromObjective(data.id)).success(function(data) {
                obj.glossitems = data.objects;
            });
            $http.get(edjectiveAppUrls.getTrueFalseItemsFromObjective(data.id)).success(function(data) {
                obj.tfitems = data.objects;
            });
            $http.get(edjectiveAppUrls.getMultipleChoiceItemsFromObjective(data.id)).success(function(data) {
                obj.mcitems = data.objects;
            });
        };
    }

    $scope.classSelection = function(cl) {
        // Key data is cl.name and cl.isSelected
        if (cl.isSelected) {
            var curdate = new Date();
            var curdatestr = $filter('date')(curdate, 'yyyy-MM-dd');
            var weekago = new Date();
            weekago.setDate(weekago.getDate() - 7);
            var weekagostr = $filter('date')(weekago, 'yyyy-MM-dd');
            $http.get(edjectiveAppUrls.getObjectivesFromTeacherClass($scope.teacher_email, weekagostr, curdatestr, cl.name)).success(function(data) {
                var newobj = {'text': cl.name, 'objectives': []};
                for (var i = 0; i < data.meta.total_count; i++) {
                    newobj.objectives.push({'date': data.objects[i].date, 'objective': data.objects[i].objective,
                                            'comments': data.objects[i].comments});
                    $http.get(edjectiveAppUrls.getObjective(data.objects[i].objective)).success(annotate_objective($http, data, newobj.objectives[newobj.objectives.length - 1]));
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
        $scope.objectives = {'data': []};
        $scope.notice = {'text': 'Loading ' + args + '...'};

        $http.get("resources/config.json").success(function(data) {

            edjectiveAppUrls.setBase(data['base_api_url']);

            $http.get(edjectiveAppUrls.getClassesFromTeacher(args)).success(function(data) {
                if (data.meta.total_count == 0) {
                    $scope.notice = {'text': 'The teacher e-mail address is invalid.'};
                }
                else {
                    $scope.notice = {'text': "Select one or more of this teacher's classes:"};
                    $scope.classes = data.objects;
                }
            }).error(function () {
                $scope.notice.text = 'The server could not be contacted.';
            });

        }).error(function () {
            $scope.notice.text = 'The server could not be contacted.';
        });
    });
});

edjectiveApp.controller('FlashcardCtrl', function ($scope, Flashcards) {
    $scope.flashcards_service = Flashcards;
    $scope.flashcards = $scope.flashcards_service.get();
    $scope.have_flashcards = $scope.flashcards.length > 0;
    $scope.min = 0;
    $scope.max = $scope.flashcards.length - 1;
    $scope.front_back = 0;
    $scope.current = 0;
    $scope.deck_status = '';

    $scope.update_status = function() {
        $scope.deck_status = '' + ($scope.current + 1) + ' of ' + $scope.flashcards.length;
    };

    $scope.previousFlashcard = function() {
        if ($scope.current > $scope.min) {
            $scope.current--;
            $scope.front_back = 0;
            $scope.update_status();
        }
    };
    $scope.nextFlashcard = function() {
        if ($scope.current < $scope.max) {
            $scope.current++;
            $scope.front_back = 0;
            $scope.update_status();
        }
    };
    $scope.flipFlashcard = function() {
        $scope.front_back = 1 - $scope.front_back;
    };
    $scope.removeFlashcard = function() {
        $scope.flashcards.splice($scope.current, 1);
        if ($scope.current > 0) {
            $scope.current--;
        }
        $scope.max--;
        $scope.front_back = 0;
        $scope.have_flashcards = $scope.flashcards.length > 0;
        $scope.update_status();
    };

    $scope.update_status();
});
