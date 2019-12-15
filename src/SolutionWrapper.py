import numpy as np

from src.RandomProblemGenerator import RandomProblemGenerator
from src.Truck import Truck


class SolutionWrapper:
    def __init__(self, solution, problem_instance):
        for index in range(0, len(solution)):
            if solution[index] > 1:
                solution[index] = 1
            elif solution[index] < 0:
                solution[index] = 0
        print(solution)

        self.inbound_truck_list = self._prepare_truck_lists(solution[0:2 * problem_instance['N']], problem_instance, 'N', 'R', 'a', 'b')
        print("KAMIL2", len(solution[0:2 * problem_instance['N']]))
        self.outbound_truck_list = self._prepare_truck_lists(solution[2 * problem_instance['N']:2 * problem_instance['N']+2 * problem_instance['M']], problem_instance, 'M', 'S', 'c', 'd')
        print("KAMIL2", len(solution[2 * problem_instance['N']:2 * problem_instance['N']+2 * problem_instance['M']]))

        inbound_products = np.array([0] * problem_instance['K'])
        for dock in self.inbound_truck_list:
            for truck in dock:
                for elem in truck.product_list:
                    inbound_products[elem[0]] += elem[1]

        outbound_products = np.array([0] * problem_instance['K'])
        for dock in self.outbound_truck_list:
            for truck in dock:
                for elem in truck.product_list:
                    outbound_products[elem[0]] += elem[1]

        for elem1, elem2 in zip(inbound_products, outbound_products):
            if elem1 != elem2:
                print("elem1 = ", elem1)
                print("elem2 = ", elem2)
                print("INBOUND = ", inbound_products, sum(inbound_products))
                print("OUTBOUND = ", outbound_products, sum(outbound_products))
            assert(elem1 == elem2)

        if sum(inbound_products) != sum(outbound_products):
            print("INBOUND = ", inbound_products)
            print("OUTBOUND = ", outbound_products)
        assert(sum(inbound_products) == sum(outbound_products))

    def get_inbound_truck_list(self, dock_index):
        return self.inbound_truck_list[dock_index]

    def get_outbound_truck_list(self, dock_index):
        return self.outbound_truck_list[dock_index]

    @staticmethod
    def _prepare_truck_lists(solution, problem_instance, truck_num_var, dock_num_var, priority_var, num_prod_var):
        truck_dock_association = solution[0:problem_instance[truck_num_var]]
        print("KAMIL", len(solution[0:problem_instance[truck_num_var]]))

        truck_dock_association = [[index, int(x * problem_instance[dock_num_var])] for index, x in
                                          enumerate(truck_dock_association)]
        print("ASSOCIATION", truck_dock_association)
        priorites = solution[problem_instance[truck_num_var]:]
        trucks_list = []
        trucks_for_inbound_docks = []
        for dock_id in range(0, problem_instance[dock_num_var]):
            trucks_for_inbound_docks.append([])
            trucks_list.append([])
            for association in truck_dock_association:
                if association[1] == dock_id:
                    trucks_for_inbound_docks[dock_id].append([association[0], priorites[association[0]]])
            trucks_for_inbound_docks[dock_id].sort(key=lambda x: x[1])
            for truck in trucks_for_inbound_docks[dock_id]:
                trucks_list[dock_id].append(
                    Truck(problem_instance[num_prod_var][truck[0]], problem_instance[priority_var][truck[0]]))

        return trucks_list


lista = [1, 2, 3, 4, 5]
print(lista[0:2])
print(lista[2:])

random_gen = RandomProblemGenerator(5, 6, 13, 14, 10, 2, 2, 1, 1, 50, 100)
random_gen.read_json('problem.json')
problem_inst = random_gen.get_problem_instance()
print(problem_inst)

x = [1., 0.62580164, 1., 1., 1., 1.,
     0.91522889, 0.00934208, 0.00153406, 0.38981709, 0.54745056, 0.67962871,
     1., 0.75882969, 0.43754228, 0.79345035, 1., 0.3323289,
     1., 0.94141155, 0.9165837, 0.86402804, 1., 0.6937363,
     1., 1., 1., 0.5831504, 1., 1.,
     1., 0.03550056, 1., 1., 0.92644644, 0.0757241,
     1., 1., 0.01497229, 0.33061915, 0.19645654, 0.93154991,
     0.61970576, 0.84949226, 0.49143833, 0.78254829, 1., 0.76788574,
     1., 0.82162909, 0.56431767, 0.12836576, 0.6360821, 0.65741122]

wrap = SolutionWrapper(x, problem_inst)