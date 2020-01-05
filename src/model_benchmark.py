from CrossDockingCentre import CrossDockingCentre
from RandomProblemGenerator import RandomProblemGenerator
from SolutionWrapper import SolutionWrapper
from random import random
from tqdm import tqdm
import time
import matplotlib.pyplot as plt


def check_time_vs_num_trucks():
    times = []
    for num_trucks in tqdm(range(10, 1001, 10)):
        random_gen = RandomProblemGenerator(3, 3, num_trucks, num_trucks, 10, 2, 2, 1, 1, num_trucks * 10,
                                            num_trucks * 10)
        random_gen.randomize()
        problem_inst = random_gen.get_problem_instance()
        centre = CrossDockingCentre(problem_inst)
        suma = 0
        for _ in range(5):
            wrap = SolutionWrapper([random() for _ in range(num_trucks * 4)], problem_inst)
            centre.load_solution(wrap)
            start = time.time()
            centre.simulate()
            end = time.time()
            suma += end - start
        avg = suma / 5
        times.append(avg)
    return range(10, 1001, 10), times


def check_time_vs_num_docks():
    times = []
    num_trucks = 300
    for num_docks in tqdm(range(1, 501)):
        random_gen = RandomProblemGenerator(num_docks, num_docks, num_trucks, num_trucks, 10, 2, 2, 1, 1, num_trucks * 10,
                                            num_trucks * 10)
        random_gen.randomize()
        problem_inst = random_gen.get_problem_instance()
        centre = CrossDockingCentre(problem_inst)
        suma = 0
        for _ in range(5):
            wrap = SolutionWrapper([random() for _ in range(num_trucks * 4)], problem_inst)
            centre.load_solution(wrap)
            start = time.time()
            centre.simulate()
            end = time.time()
            suma += end - start
        avg = suma / 5
        times.append(avg)
    return range(1, 501), times


if __name__ == "__main__":
    x, y = check_time_vs_num_docks()
    plt.plot(x, y)
    plt.show()
