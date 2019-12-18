import random
import numpy as np


class Particle:
    def __init__(self, span_size, cost_function):
        self.velocity = np.array([0] * span_size)
        self.position = np.array([random.random() for _ in range(0, span_size)])
        self.cost_function = cost_function
        self.cost = self.cost_function(self.position)
        self.best_position = self.position
        self.best_cost = self.cost

    def update_personal_best(self):
        if self.cost < self.best_cost:
            self.best_cost = self.cost
            self.best_position = self.position
            return True
        return False

    def update(self, global_best_pos, inertia, c1, c2):
        self.velocity = inertia * self.velocity + \
                        c1 * random.random() * self.best_position - self.position + \
                        c2 * random.random() * global_best_pos - self.position

        self.position = self.position + self.velocity
        self.cost = self.cost_function(self.position)
        return self.update_personal_best()
