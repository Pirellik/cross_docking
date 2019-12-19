import numpy as np
from tqdm import tqdm
from run import CostFcnWrapper


class SimulatedAnnealingOptimizer:
    def __init__(self, max_iter, min_val=0, max_val=0.99999):
        self.max_iter = max_iter
        self.min_val = min_val
        self.max_val = max_val

    def optimize(self, cost_function, initial_solution):
        state = initial_solution
        cost = cost_function(state)
        print("INITIAL COST = ", cost)
        for iter_num in tqdm(range(self.max_iter)):
            fraction = iter_num / float(self.max_iter)
            T = self.temperature(fraction)
            new_state = self.random_neighbour(state, fraction)
            new_cost = cost_function(new_state)
            if self.acceptance_probability(cost, new_cost, T) > np.random.random():
                state, cost = new_state, new_cost

        return state, cost_function(state)

    def random_neighbour(self, x, fraction):
        amplitude = (self.max_val - self.min_val) * fraction / 10.0
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


if __name__ == "__main__":
    cost_fcn_wrapper = CostFcnWrapper()
    opt = SimulatedAnnealingOptimizer(20000)
    print(opt.optimize(cost_fcn_wrapper.cost_function, np.array([np.random.random() for _ in range(106)])))