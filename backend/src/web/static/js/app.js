angular.module("app", []);

angular.module("app").config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{').endSymbol('}');
});

angular.module("app").controller('MathController', function($scope, $window, $http){

    var operation_map = {
        'multiplication': '*',
        'addition': '+',
        'division': '/',
        'subtraction': '-'
    };

    $scope.answer = function(choice_index){
        $http({
            url: '/api/solve_problem',
            method: 'GET',
            params: {problem_id: $scope.problem.id, answer: $scope.problem.choices[choice_index]}
        }).success(function(result){
            if (result.is_correct){
                alert("Você acertou");
            }else{
                alert("Você errou");
            }
        }).finally(function(){
            $window.location.reload();
        });
    };

    $window.onload = function(){
      $http({
          url: '/api/create_problem',
          method: 'GET',
          params: {level: level, kind: kind}
      }).success(function(result){
            $scope.problem = result;
            $scope.problem.operation = operation_map[$scope.problem.kind];
      });
    };
});