from RandomProblemGenerator import RandomProblemGenerator
from SolutionWrapper import SolutionWrapper
from CrossDockingCentre import CrossDockingCentre
from ParticleSwarmOptimizer import ParticleSwarmOptimizer
from SimulatedAnnealingOptimizer import SimulatedAnnealingOptimizer
import json, os
#import matplotlib.pyplot as plt
import numpy as np
import time


class CostFcnWrapper:
    def __init__(self, problem, log_tmp_storage=False, problem_nickname=None):
        self.log_tmp_storage = log_tmp_storage
        self.problem_nickname = problem_nickname
        self.problem_instance = problem

    def cost_function(self, x):
        wrap = SolutionWrapper(x, self.problem_instance)
        centre = CrossDockingCentre(self.problem_instance)
        centre.load_solution(wrap)
        cost = centre.simulate(self.log_tmp_storage)
        return cost


class PsoBestCostsDumper:
    def __init__(self, problem_name):
        self.problem_name = problem_name
        self.costs = {"iterations": [], "costs": [], "time": []}
        self.iter = 1
        self.start_time = time.time()

    def dump(self, pso, last_iter):
        if not last_iter:
            self.costs["iterations"].append(self.iter)
            self.costs["costs"].append(pso.global_best_cost)
            self.costs["time"].append(time.time() - self.start_time)
        else:
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + \
                       'results/PSO/' + self.problem_name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'pso_best_costs.json', 'w') as outfile:
                json.dump(self.costs, outfile)
        self.iter += 1


class PsoParticlesDumper:
    def __init__(self, problem_name):
        self.problem_name = problem_name
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
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + \
                       'results/PSO/' + self.problem_name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'best_particles.json', 'w') as outfile:
                json.dump(self.best_particles, outfile)
        self.iter += 1


class BestSolutionSaver:
    def __init__(self, problem_name):
        self.problem_name = problem_name

    def best_solution_saver(self, pso, last_iter):
        if last_iter:
            solution = {'solution': list(pso.global_best_position), 'cost': pso.global_best_cost}
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + \
                       'results/PSO/' + self.problem_name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'best_solution.json', 'w') as outfile:
                json.dump(solution, outfile)


if __name__ == "__main__":

    # Standard PSO

    for problem_name in os.listdir(r"problems/"):
        print(problem_name)
        best_sol_dumper = PsoBestCostsDumper(problem_name[:-5])
        particles_dumper = PsoParticlesDumper(problem_name[:-5])
        saver = BestSolutionSaver(problem_name[:-5])
        random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
        random_gen.read_json(r"problems/" + problem_name)
        problem_inst = random_gen.get_problem_instance()
        cost_fcn_wrapper = CostFcnWrapper(problem_inst)
        opt = ParticleSwarmOptimizer(problem_inst['N'] * 4,
                                     cost_fcn_wrapper.cost_function,
                                     max_iter=100,
                                     population_size=int(problem_inst['N'] / 2),
                                     callbacks=[best_sol_dumper.dump,
                                                particles_dumper.dump,
                                                saver.best_solution_saver])
        print(opt.optimize())
        print("\n")

    # # Hybrid PSO
    #
    # for problem_name in os.listdir(r"problems/"):
    #     print(problem_name)
    #     best_sol_dumper = PsoBestCostsDumper(problem_name[:-5])
    #     particles_dumper = PsoParticlesDumper(problem_name[:-5])
    #     saver = BestSolutionSaver(problem_name[:-5])
    #     random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
    #     random_gen.read_json(r"problems/" + problem_name)
    #     problem_inst = random_gen.get_problem_instance()
    #     cost_fcn_wrapper = CostFcnWrapper(problem_inst)
    #     local_opt = SimulatedAnnealingOptimizer(100)
    #     opt = ParticleSwarmOptimizer(problem_inst['N'] * 4,
    #                                  cost_fcn_wrapper.cost_function,
    #                                  max_iter=1000,
    #                                  population_size=16,
    #                                  local_search_alg=local_opt.optimize,
    #                                  callbacks=[best_sol_dumper.dump,
    #                                             particles_dumper.dump,
    #                                             saver.best_solution_saver])
    #     opt.optimize()
    #     print("\n")
