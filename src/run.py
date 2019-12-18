from src.RandomProblemGenerator import RandomProblemGenerator
from src.SolutionWrapper import SolutionWrapper
from src.CrossDockingCentre import CrossDockingCentre
from src.ParticleSwarmOptimizer import ParticleSwarmOptimizer


if __name__ == "__main__":
    random_gen = RandomProblemGenerator(5, 6, 24, 29, 10, 2, 2, 1, 1, 120, 150)
    random_gen.randomize()
    problem_inst = random_gen.get_problem_instance()

    def cost_function(x):
        wrap = SolutionWrapper(x, problem_inst)
        centre = CrossDockingCentre(problem_inst)
        centre.load_solution(wrap)
        return centre.simulate()

    opt = ParticleSwarmOptimizer(106, cost_function, 15, 1.1, 1.25, 1.25, 1000)
    print(opt.optimize())