from RandomProblemGenerator import RandomProblemGenerator
from SolutionWrapper import SolutionWrapper
from CrossDockingCentre import CrossDockingCentre
from ParticleSwarmOptimizer import ParticleSwarmOptimizer


random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
random_gen.randomize()
problem_inst = random_gen.get_problem_instance()


def cost_function(x):
    wrap = SolutionWrapper(x, problem_inst)
    centre = CrossDockingCentre(problem_inst)
    centre.load_solution(wrap)
    return centre.simulate()


if __name__ == "__main__":
    opt = ParticleSwarmOptimizer(106, cost_function)
    opt.optimize()
