from src.TemporaryStorage import TemporaryStorage
from src.InboundDock import InboundDock
from src.OutboundDock import OutboundDock


class CrossDockingCentre:
    def __init__(self, problem_instance):
        self.temporary_storage = TemporaryStorage(problem_instance['K'])
        self.time_step = min(problem_instance['G'], problem_instance['U'], problem_instance['F'], problem_instance['V'])
        self.inbound_docks = [InboundDock(problem_instance['G'],
                                          problem_instance['U'],
                                          self.temporary_storage) for _ in range(0, problem_instance['R'])]

        self.outbound_docks = [OutboundDock(problem_instance['F'],
                                            problem_instance['V'],
                                            self.time_step,
                                            self.temporary_storage) for _ in range(0, problem_instance['S'])]

        self.num_docks = len(self.inbound_docks) + len(self.outbound_docks)

    def load_solution(self, solution_wrapper):
        for index, dock in enumerate(self.inbound_docks):
            dock.load_truck_list(solution_wrapper.get_inbound_truck_list(index))

        for index, dock in enumerate(self.outbound_docks):
            dock.load_truck_list(solution_wrapper.get_outbound_truck_list(index))

    def simulate(self):
        time = 0
        docks_finished = 0

        while self.inbound_docks:#docks_finished < 5:#self.num_docks:
            print('==========================================================================')
            for index, dock in enumerate(self.inbound_docks):
                if dock.is_operation_finished():
                    docks_finished += 1
                    self.inbound_docks.pop(index)
                else:
                    print(dock.state)
                    dock.process_unloading_operation(time)
            # for index, dock in enumerate(self.outbound_docks):
            #     if dock.are_operations_finished():
            #         docks_finished += 1
            #         self.outbound_docks.pop(index)
            #     else:
            #         dock.process_loading_operation(time)

            time += self.time_step
            # print("iteracja kolejna, wartosc docks_finished = ", docks_finished)
            print("DLUGOSC INBOUND = ", len(self.inbound_docks))
            print("DLUGOSC OUTBOUND = ", len(self.outbound_docks))

        return time - self.time_step


# random_gen = RandomProblemGenerator(5, 6, 13, 14, 10, 2, 2, 1, 1, 70, 150)
# random_gen.randomize()
# problem_inst1 = random_gen.get_problem_instance()
# cross = CrossDockingCentre(problem_inst1)
#
# for elem in cross.inbound_docks:
#     print(elem.truck_list)