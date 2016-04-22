angular.module("app", []);

angular.module("app").config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{').endSymbol('}');
});

angular.module("app").controller('MathController', function($scope, $window, $http, $interval){

    var operation_map = {
        'multiplication': '*',
        'addition': '+',
        'division': '/',
        'subtraction': '-'
    };
    var math_problem_set_id, problem_index;
    var quantity = 10;
    $scope.time_spent = 0;

    $interval(function(){
        $scope.time_spent ++;
    }, 1000);


    $scope.answer = function(choice_index){
        $http({
            url: '/api/solve_problem',
            method: 'GET',
            params: {
                problem_id: $scope.problem.id,
                answer: $scope.problem.choices[choice_index],
                problem_set_id: math_problem_set_id}
        }).success(function(result){
            if (result.is_correct){
                alert("Você acertou");
            }else{
                alert("Você errou");
            }
        }).finally(function(){
            problem_index++;
            if (problem_index == quantity){
                save_time_spent($scope.time_spent).success(function(){
                    $window.location.href = '/resultados/' + math_problem_set_id;
                });
            }else{
                _get_problem(problem_index);
            }
        });
    };

	var _get_problem = function(index){
		return $http({
			url: '/api/get_problem',
			method: 'GET',
			params: {math_problem_set_id: math_problem_set_id, index: index}
		}).success(function(result){
            $scope.problem = result;
            $scope.problem.operation = operation_map[$scope.problem.kind];
		});
	};

    var save_time_spent = function(time_spent){
        return $http({
            url: '/api/save_time_spent',
            method: 'GET',
            params: {time_spent: time_spent, math_problem_set_id: math_problem_set_id}
        })
    };

    var _get_problem_set = function(){
      return $http({
            url: '/api/create_problem_set',
            method: 'GET',
            params: {level: level, kind: kind, quantity: quantity}
        }).success(function(result){
            problem_index = 0;
            $scope.problem = result.problem;
            math_problem_set_id = result.math_problem_set_id;
            $scope.problem.operation = operation_map[$scope.problem.kind];
        });  
    }
	$window.onload = function(){
		_get_problem_set();
	};
});