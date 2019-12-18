import numpy as np
from Truck import Truck


class SolutionWrapper:
    def __init__(self, solution, problem_instance):
        for index in range(0, len(solution)):
            if solution[index] >= 1:
                solution[index] = 0.999
            elif solution[index] < 0:
                solution[index] = 0

        self.inbound_truck_list = self._prepare_truck_lists(solution[0:2 * problem_instance['N']], problem_instance, 'N', 'R', 'a', 'b')
        self.outbound_truck_list = self._prepare_truck_lists(solution[2 * problem_instance['N']:2 * problem_instance['N']+2 * problem_instance['M']], problem_instance, 'M', 'S', 'c', 'd')

    def get_inbound_truck_list(self, dock_index):
        return self.inbound_truck_list[dock_index]

    def get_outbound_truck_list(self, dock_index):
        return self.outbound_truck_list[dock_index]

    @staticmethod
    def _prepare_truck_lists(solution, problem_instance, truck_num_var, dock_num_var, priority_var, num_prod_var):
        truck_dock_association = solution[0:problem_instance[truck_num_var]]

        truck_dock_association = [[index, int(x * problem_instance[dock_num_var])] for index, x in
                                          enumerate(truck_dock_association)]
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
