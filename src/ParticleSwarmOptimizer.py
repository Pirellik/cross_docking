from Particle import Particle
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool


def update_particle(particle):
    return particle.update()


class ParticleSwarmOptimizer:
    def __init__(self, span_size, cost_function, population_size=20, inertia=1, c1=1.3, c2=1.3, max_iter=1000):
        self.global_best_cost = 2 ** 64
        self.global_best_position = np.array([0] * span_size)
        self.particles = []
        for _ in range(0, population_size):
            self.particles.append(Particle(span_size, cost_function, inertia, c1, c2))
            if self.particles[-1].best_cost < self.global_best_cost:
                self.global_best_cost = self.particles[-1].best_cost
                self.global_best_position = self.particles[-1].best_position
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter

    def optimize(self):
        pool = Pool(8)
        pbar = tqdm(total = self.max_iter)
        pbar.set_description(f'CURRENT BEST = {self.global_best_cost}')
        for _ in range(0, self.max_iter):
            for particle in self.particles:
                particle.load_global_best_pos(self.global_best_position)
            self.particles = pool.map(update_particle, self.particles)
            for particle in self.particles:
                if particle.improved:
                    self.update_global_best(particle)
                    pbar.set_description(f'CURRENT BEST = {self.global_best_cost}')
            pbar.update()
        return self.global_best_cost

    def update_global_best(self, particle):
        if particle.best_cost < self.global_best_cost:
            self.global_best_cost = particle.best_cost
            self.global_best_position = particle.best_position
