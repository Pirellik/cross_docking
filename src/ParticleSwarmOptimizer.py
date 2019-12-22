from Particle import Particle
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool
import multiprocessing


def update_particle(particle):
    return particle.update()


class ParticleSwarmOptimizer:
    def __init__(self, span_size,
                 cost_function,
                 min_val=0,
                 max_val=0.99999,
                 population_size=16,
                 inertia=1,
                 c1=1.3,
                 c2=1.3,
                 max_iter=1000,
                 local_search_alg=None,
                 **kwargs):

        self.global_best_cost = 2 ** 64
        self.global_best_position = np.array([0] * span_size)
        self.particles = []
        for _ in range(0, population_size):
            self.particles.append(Particle(span_size, cost_function, inertia, c1, c2, min_val, max_val, local_search_alg))
            if self.particles[-1].best_cost < self.global_best_cost:
                self.global_best_cost = self.particles[-1].best_cost
                self.global_best_position = self.particles[-1].best_position
        self.inertia = inertia
        self.c1 = c1
        self.c2 = c2
        self.max_iter = max_iter
        self.callbacks = []
        for key, value in kwargs.items():
            if key == 'callbacks':
                self.callbacks = value

    def optimize(self):
        print('INITIAL SOLUTION COST = ', self.global_best_cost)
        pool = Pool(multiprocessing.cpu_count())
        pbar = tqdm(total=self.max_iter)
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
            for callback in self.callbacks:
                callback(self, False)
        for callback in self.callbacks:
            callback(self, last_iter=True)
        return self.global_best_cost

    def update_global_best(self, particle):
        if particle.best_cost < self.global_best_cost:
            self.global_best_cost = particle.best_cost
            self.global_best_position = particle.best_position
