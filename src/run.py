import numpy as np

from src.RandomProblemGenerator import RandomProblemGenerator
from src.SolutionWrapper import SolutionWrapper
from src.CrossDockingCentre import CrossDockingCentre
from src.ParticleSwarmOptimizer import ParticleSwarmOptimizer
from src.Particle import Particle
import random


if __name__ == "__main__":
    # random_gen = RandomProblemGenerator(5, 6, 13, 14, 10, 2, 2, 1, 1, 50, 100)
    # # random_gen.randomize()
    # random_gen.read_json('problem.json')
    # problem_inst = random_gen.get_problem_instance()
    # print(problem_inst)
    # centre = CrossDockingCentre(problem_inst)
    #
    # for _ in range(0, 100):
    #     wrap = SolutionWrapper([random.random() for _ in range(0, 54)], problem_inst)
    #     centre = CrossDockingCentre(problem_inst)
    #     centre.load_solution(wrap)
    #     time = centre.simulate()
    #     print("TIME = ", time)
    #
    # x = [1., 0.62580164, 1., 1., 1., 1.,
    #      0.91522889, 0.00934208, 0.00153406, 0.38981709, 0.54745056, 0.67962871,
    #      1., 0.75882969, 0.43754228, 0.79345035, 1., 0.3323289,
    #      1., 0.94141155, 0.9165837, 0.86402804, 1., 0.6937363,
    #      1., 1., 1., 0.5831504, 1., 1.,
    #      1., 0.03550056, 1., 1., 0.92644644, 0.0757241,
    #      1., 1., 0.01497229, 0.33061915, 0.19645654, 0.93154991,
    #      0.61970576, 0.84949226, 0.49143833, 0.78254829, 1., 0.76788574,
    #      1., 0.82162909, 0.56431767, 0.12836576, 0.6360821, 0.65741122]
    #
    # wrap = SolutionWrapper(x, problem_inst)
    # def cost_function(x):
    #     wrap = SolutionWrapper(x, problem_inst)
    #     centre = CrossDockingCentre(problem_inst)
    #     centre.load_solution(wrap)
    #     print("==========================================")
    #     for dock in centre.inbound_docks:
    #         print(len(dock.truck_list))
    #     print("------------------------------------------")
    #     for dock in centre.outbound_docks:
    #         print(len(dock.truck_list))
    #     print("==========================================")
    #
    #     return centre.simulate()
    #
    #
    # # particle = Particle(54, cost_function)
    # # for _ in range(0, 5):
    # #     particle.update(particle.best_position, 1, 1, 1)
    # #     print(particle.best_cost)
    # #     # print(cost_function(np.array([random.random() for _ in range(0, 54)])))
    #
    # opt = ParticleSwarmOptimizer(54, cost_function, 2, 1, 2, 2, 2)
    # print(opt.optimize())