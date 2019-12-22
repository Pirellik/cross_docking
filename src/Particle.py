import random
import numpy as np


class Particle:
    def __init__(self, span_size, cost_function, inertia, c1, c2, min_val, max_val, local_search_alg):
        self.velocity = np.array([0] * span_size)
        self.position = np.array([random.random() for _ in range(0, span_size)])
        self.cost_function = cost_function
        self.cost = self.cost_function(self.position)
        self.best_position = self.position
        self.best_cost = self.cost
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.improved = False
        self.global_best_pos = self.position
        self.min_val = min_val
        self.max_val = max_val
        self.local_search_alg = local_search_alg

    def update_personal_best(self):
        if self.cost < self.best_cost:
            self.best_cost = self.cost
            self.best_position = self.position
            return True
        return False

    def load_global_best_pos(self, global_best_pos):
        self.global_best_pos = global_best_pos

    def update(self):
        self.velocity = self.inertia * self.velocity + \
                        self.c1 * random.random() * self.best_position - self.position + \
                        self.c2 * random.random() * self.global_best_pos - self.position

        self.position = np.clip(self.position + self.velocity, a_min=self.min_val, a_max=self.max_val)

        if self.local_search_alg is None:
            self.cost = self.cost_function(self.position)
        else:
            self.position, self.cost = self.local_search_alg(self.cost_function, self.position)

        self.improved = self.update_personal_best()
        return self


