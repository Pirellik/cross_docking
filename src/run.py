from RandomProblemGenerator import RandomProblemGenerator
from SolutionWrapper import SolutionWrapper
from CrossDockingCentre import CrossDockingCentre
from ParticleSwarmOptimizer import ParticleSwarmOptimizer
import json, os
import matplotlib.pyplot as plt
import numpy as np


random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
random_gen.randomize()
problem_inst = random_gen.get_problem_instance()


class CostFcnWrapper:
    def __init__(self, log_tmp_storage=False, problem_nickname=None):
        self.log_tmp_storage = log_tmp_storage
        self.problem_nickname = problem_nickname

    def cost_function(self, x):
        wrap = SolutionWrapper(x, problem_inst)
        centre = CrossDockingCentre(problem_inst)
        centre.load_solution(wrap)
        time = centre.simulate(self.log_tmp_storage)
        if self.log_tmp_storage:
            dir_path = __file__.replace(__file__.split('/')[-1], '')\
                           .replace(__file__.split('/')[-2] + '/', '') + 'results/' + self.problem_nickname + "/"
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'tmp_storage_log.json', 'w') as outfile:
                json.dump(centre.tmp_storage_log, outfile)
        return time


class PsoBestCostsDumper:
    def __init__(self):
        self.costs = {"iterations": [], "costs": []}
        self.iter = 1

    def dump(self, pso, last_iter):
        if not last_iter:
            self.costs["iterations"].append(self.iter)
            self.costs["costs"].append(pso.global_best_cost)
        else:
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + 'results/'
            with open(dir_path + 'pso_best_costs.json', 'w') as outfile:
                json.dump(self.costs, outfile)
        self.iter += 1


class PsoParticlesDumper:
    def __init__(self):
        self.best_particles = {"iterations": [], "min_costs": [], "max_costs": [], "avg_costs": [], "med_costs": []}
        self.iter = 1

    def dump(self, pso, last_iter):
        if not last_iter:
            particles_costs = [particle.cost for particle in pso.particles]
            self.best_particles["iterations"].append(self.iter)
            self.best_particles["min_costs"].append(float(np.min(particles_costs)))
            self.best_particles["max_costs"].append(float(np.max(particles_costs)))
            self.best_particles["avg_costs"].append(float(np.average(particles_costs)))
            self.best_particles["med_costs"].append(float(np.median(particles_costs)))
        else:
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + 'results/'
            with open(dir_path + 'best_particles.json', 'w') as outfile:
                json.dump(self.best_particles, outfile)
        self.iter += 1


def best_solution_saver(pso, last_iter):
    if last_iter:
        solution = {'solution': list(pso.global_best_position), 'cost': pso.global_best_cost}
        dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + 'results/'
        with open(dir_path + 'best_solution.json', 'w') as outfile:
            json.dump(solution, outfile)


if __name__ == "__main__":
    cost_fcn_wrapper = CostFcnWrapper()
    best_sol_dumper = PsoBestCostsDumper()
    particles_dumper = PsoParticlesDumper()
    opt = ParticleSwarmOptimizer(106, cost_fcn_wrapper.cost_function, callbacks=[best_sol_dumper.dump,
                                                                                 particles_dumper.dump,
                                                                                 best_solution_saver])
    opt.optimize()
    # path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + 'results/'
    # # with open(path + 'best_particles.json', 'r') as infile:
    # #     best_part = json.load(infile)
    # # plt.plot(best_part['iterations'], best_part['med_costs'])
    # with open(path + 'pso_best_costs.json', 'r') as infile:
    #     best_part = json.load(infile)
    # plt.plot(best_part['iterations'], best_part['costs'])
    # plt.show()
