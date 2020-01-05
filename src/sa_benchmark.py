from RandomProblemGenerator import RandomProblemGenerator
from SolutionWrapper import SolutionWrapper
from CrossDockingCentre import CrossDockingCentre
from ParticleSwarmOptimizer import ParticleSwarmOptimizer
from SimulatedAnnealingOptimizer import SimulatedAnnealingOptimizer
import json, os, random
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


class SaCostsDumper:
    def __init__(self, problem_name):
        self.problem_name = problem_name
        self.costs = {"iterations": [], "costs": [], "best_costs": [], "time": []}
        self.iter = 1
        self.start_time = time.time()

    def dump(self, sa, last_iter):
        if not last_iter:
            self.costs["iterations"].append(self.iter)
            self.costs["costs"].append(sa.cost)
            self.costs["best_costs"].append(sa.best_cost)
            self.costs["time"].append(time.time() - self.start_time)
        else:
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + \
                       'results/SA/' + self.problem_name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'sa_costs.json', 'w') as outfile:
                json.dump(self.costs, outfile)
        self.iter += 1


class BestSolutionSaver:
    def __init__(self, problem_name):
        self.problem_name = problem_name

    def best_solution_saver(self, sa, last_iter):
        if last_iter:
            solution = {'solution': list(sa.best_state), 'cost': sa.best_cost}
            dir_path = __file__.replace(__file__.split('/')[-1], '').replace(__file__.split('/')[-2] + '/', '') + \
                       'results/SA/' + self.problem_name + '/'
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)
            with open(dir_path + 'best_solution.json', 'w') as outfile:
                json.dump(solution, outfile)


if __name__ == "__main__":
    for problem_name in os.listdir(r"problems/"):
        print(problem_name)
        costs_dumper = SaCostsDumper(problem_name[:-5])
        saver = BestSolutionSaver(problem_name[:-5])
        random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
        random_gen.read_json(r"problems/" + problem_name)
        problem_inst = random_gen.get_problem_instance()
        cost_fcn_wrapper = CostFcnWrapper(problem_inst)
        opt = SimulatedAnnealingOptimizer(100, callbacks=[costs_dumper.dump,
                                                           saver.best_solution_saver])
        print(opt.optimize(cost_fcn_wrapper.cost_function, [random.random() for _ in range(problem_inst['N'] * 4)]))
        print("\n")