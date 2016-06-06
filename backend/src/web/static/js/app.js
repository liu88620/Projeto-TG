angular.module("app", ['rest_api']);

angular.module("app").config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{').endSymbol('}');
});

angular.module("app").controller('MathController', function ($scope, $window, $interval, RestApi) {

    var operation_map = {
        'multiplication': '*',
        'addition': '+',
        'division': '/',
        'subtraction': '-'
    };

    var level_map = {
        'facil': 'easy',
        'medio': 'medium',
        'dificil': 'hard'
    };

    var math_problem_set_id, problem_index;
    var quantity_of_questions = 10;
    $scope.time_spent = 0;

    $interval(function () {
        $scope.time_spent++;
    }, 1000);


    $scope.answer = function(choice_index){
        var answer = $scope.problem.choices[choice_index];
        RestApi.solve_problem($scope.problem.id, math_problem_set_id, answer).success(function (result) {
            if (result.is_correct){
                alert("Você acertou");
            }else{
                alert("Você errou");
            }
        }).finally(function(){
            problem_index++;
            if (problem_index == quantity_of_questions) {
                RestApi.save_time_spent($scope.time_spent, math_problem_set_id).success(function () {
                    $window.location.href = '/resultados/' + math_problem_set_id;
                });
            } else {
                _get_problem(problem_index);
            }
        });
    };

    var _get_problem = function (index) {
        RestApi.get_problem(math_problem_set_id, index).success(function (result) {
            $scope.problem = result;
            $scope.problem.operation = operation_map[$scope.problem.kind];
        });
    };

    var _get_problem_set = function () {
        RestApi.get_problem_set(level_map[level], kind, quantity_of_questions).success(function (result) {
            problem_index = 0;
            $scope.problem = result.problem;
            math_problem_set_id = result.math_problem_set_id;
            $scope.problem.operation = operation_map[$scope.problem.kind];
        });
    }
    $window.onload = function () {
        _get_problem_set();
    };
});