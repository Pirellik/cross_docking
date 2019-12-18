from TemporaryStorage import TemporaryStorage
from InboundDock import InboundDock
from OutboundDock import OutboundDock
import json


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
        self.tmp_storage_log = {"time": [], 'num_items': []}

    def load_solution(self, solution_wrapper):
        for index, dock in enumerate(self.inbound_docks):
            dock.load_truck_list(solution_wrapper.get_inbound_truck_list(index))

        for index, dock in enumerate(self.outbound_docks):
            dock.load_truck_list(solution_wrapper.get_outbound_truck_list(index))

    def simulate(self, log_tmp_storage=False):
        time = 0
        docks_finished = 0

        while sum([dock.is_operation_finished() for dock in self.inbound_docks]) < len(self.inbound_docks)\
                or sum([dock.is_operation_finished() for dock in self.outbound_docks]) < len(self.outbound_docks):
            if log_tmp_storage:
                self.tmp_storage_log["time"].append(time)
                self.tmp_storage_log["num_items"].append(self.temporary_storage.products)
            for dock in self.inbound_docks:
                if dock.is_operation_finished():
                    docks_finished += 1
                else:
                    dock.process_unloading_operation(time)
            for dock in self.outbound_docks:
                if dock.is_operation_finished():
                    docks_finished += 1
                else:
                    dock.process_loading_operation(time)

            time += self.time_step
        return time - self.time_step
