angular.module("rest_api", []);

angular.module("rest_api").factory('RestApi', function($http){
    var solve_problem_url = '/api/solve_problem';
    var save_time_spent_url = '/api/save_time_spent';
    var get_problem_url = '/api/get_problem';
    var get_problem_set_url = '/api/get_problem_set';
    var api = {};

    api.solve_problem = function(problem_id, problem_set_id, answer){
        return $http({
            url: solve_problem_url,
            method: 'GET',
            params: {
                problem_id: problem_id,
                answer: answer,
                problem_set_id: problem_set_id}
        });
    };

    api.save_time_spent = function(time_spent, problem_set_id){
        return $http({
            url: save_time_spent_url,
            method: 'GET',
            params: {time_spent: time_spent, problem_set_id: problem_set_id}
        })
    };

    api.get_problem = function(problem_set_id, index){
      return $http({
			url: get_problem_url,
			method: 'GET',
			params: {problem_set_id: problem_set_id, index: index}
		})
    };

    api.get_problem_set = function(level, kind, quantity){
        return $http({
            url: get_problem_set_url,
            method: 'GET',
            params: {level: level, kind: kind, quantity: quantity}
        })
    };

    return api;
});