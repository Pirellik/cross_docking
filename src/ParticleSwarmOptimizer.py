from src.Particle import Particle
import numpy as np


class ParticleSwarmOptimizer:
    def __init__(self, span_size, cost_function, population_size, inertia, c1, c2, max_iter):
        self.global_best_cost = 2 ** 64
        self.global_best_position = np.array([0] * span_size)
        self.particles = []
        for _ in range(0, population_size):
            self.particles.append(Particle(span_size, cost_function))
            if self.particles[-1].best_cost < self.global_best_cost:
                self.global_best_cost = self.particles[-1].best_cost
                self.global_best_position = self.particles[-1].best_position
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter

    def optimize(self):
        for _ in range(0, self.max_iter):
            for particle in self.particles:
                if particle.update(self.global_best_position, self.inertia, self.c1, self.c2):
                    self.update_global_best(particle)
        return self.global_best_cost

    def update_global_best(self, particle):
        if particle.best_cost < self.global_best_cost:
            self.global_best_cost = particle.best_cost
            self.global_best_position = particle.best_position
            print("CURRENT BEST = ", self.global_best_cost)
