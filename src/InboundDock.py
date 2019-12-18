class InboundDock:
    def __init__(self, changeover_time, unloading_time, temp_storage_handle):
        self.changeover_time = changeover_time
        self.unloading_time = unloading_time
        self.truck_list = []
        self.current_job_finish_time = 0
        self.state = "INITIAL"
        self.temp_storage = temp_storage_handle
        self.operation_finished = False

    def load_truck_list(self, truck_list):
        self.truck_list = truck_list

    def is_operation_finished(self):
        return self.operation_finished

    def process_unloading_operation(self, time):
        if time != self.current_job_finish_time or self.is_operation_finished():
            return

        if self.state == "INITIAL":
            self.current_job_finish_time += self.changeover_time
            self.state = "CHANGEOVER"
            return

        if self.state == "UNLOADING":

            product = self.truck_list[0].pop_product()
            assert(product != -1)
            self.temp_storage.add_product(product)
            if self.truck_list[0].is_empty():
                self.truck_list.pop(0)
                self.current_job_finish_time += self.changeover_time
                self.state = "CHANGEOVER"
            else:
                self.current_job_finish_time += self.unloading_time

        elif self.state == "CHANGEOVER":
            self.state = "UNLOADING"
            self.current_job_finish_time += self.unloading_time
            self.operation_finished = not bool(self.truck_list)



