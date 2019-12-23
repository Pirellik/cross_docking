import numpy as np


class SimulatedAnnealingOptimizer:
    def __init__(self, max_iter, min_val=0, max_val=0.99999):
        self.max_iter = max_iter
        self.min_val = min_val
        self.max_val = max_val
        self.step_coeff = 0.05

    def optimize(self, cost_function, initial_solution):
        state = initial_solution
        cost = cost_function(state)
        best_state = state
        best_cost = cost
        # print("INITIAL COST = ", cost)
        for iter_num in range(self.max_iter):
            fraction = iter_num / float(self.max_iter)
            T = self.temperature(fraction)
            new_state = self.random_neighbour(state)
            new_cost = cost_function(new_state)
            if self.acceptance_probability(cost, new_cost, T) > np.random.random():
                state, cost = new_state, new_cost
                if new_cost < best_cost:
                    best_state, best_cost = new_state, new_cost

        return best_state, best_cost

    def random_neighbour(self, x):
        amplitude = (self.max_val - self.min_val) * self.step_coeff
        delta = np.array([- amplitude / 2.0 + amplitude * np.random.random_sample() for _ in range(len(x))])
        return np.clip(x + delta, a_min=self.min_val, a_max=self.max_val)

    @staticmethod
    def acceptance_probability(cost, new_cost, temperature):
        if new_cost < cost:
            return 1
        else:
            return np.exp(- (new_cost - cost) / temperature)

    @staticmethod
    def temperature(fraction):
        return max(0.01, min(1, 1 - fraction))

#
# if __name__ == "__main__":
#     cost_fcn_wrapper = CostFcnWrapper()
#     opt = SimulatedAnnealingOptimizer(20000)
#     print(opt.optimize(cost_fcn_wrapper.cost_function, np.array([np.random.random() for _ in range(106)])))