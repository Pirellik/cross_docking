from src.RandomProblemGenerator import RandomProblemGenerator
from src.SolutionWrapper import SolutionWrapper
from src.CrossDockingCentre import CrossDockingCentre
import random


if __name__ == "__main__":
    random_gen = RandomProblemGenerator(5, 6, 13, 14, 10, 2, 2, 1, 1, 5, 15)
    random_gen.randomize()

    problem_inst1 = random_gen.get_problem_instance()
    print(problem_inst1)

    wrap = SolutionWrapper([random.random() for _ in range(0, 54)], problem_inst1)

    centre = CrossDockingCentre(problem_inst1)
    centre.load_solution(wrap)
    time = centre.simulate()
    print('UWAGA czas = ', time)
