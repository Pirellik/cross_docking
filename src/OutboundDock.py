class OutboundDock:
    def __init__(self, changeover_time, loading_time, time_step, temp_storage_handle):
        self.changeover_time = changeover_time
        self.loading_time = loading_time
        self.truck_list = []
        self.temp_storage = temp_storage_handle
        self.current_job_finish_time = 0
        self.state = "INITIAL"
        self.time_step = time_step
        self.operations_finished = False

    def load_truck_list(self, truck_list):
        self.truck_list = truck_list

    def is_operation_finished(self):
        return self.operations_finished

    def process_loading_operation(self, time):
        # print("TIME = ", time)
        # print("FINISH TIME = ", self.current_job_finish_time)
        # print("STATE = ", self.state)
        # if self.truck_list:
        #     print("PRODUCT ID = ", self.truck_list[0].get_next_product_id())

        if time != self.current_job_finish_time or self.is_operation_finished():
            return

        if self.state == "INITIAL":
            self.on_initial()

        elif self.state == "LOADING":
            self.truck_list[0].pop_product()
            self.try_start_loading()

        elif self.state == "IDLE":
            self.try_start_loading()

        elif self.state == "CHANGEOVER":
            if not self.is_any_truck_left():
                self.operations_finished = True
            else:
                self.try_start_loading()

    def on_initial(self):
        self.current_job_finish_time += self.changeover_time
        self.state = "CHANGEOVER"

    def try_start_loading(self):
        if self.truck_list[0].is_empty():
            self.change_truck()
        elif self.try_taking_product_from_temp_storage():
            self.state = "LOADING"
            self.current_job_finish_time += self.loading_time
        else:
            self.state = "IDLE"
            self.current_job_finish_time += self.time_step

    def change_truck(self):
        self.truck_list.pop(0)
        self.current_job_finish_time += self.changeover_time
        self.state = "CHANGEOVER"

    def is_any_truck_left(self):
        return bool(self.truck_list)

    def try_taking_product_from_temp_storage(self):
        product_id = self.truck_list[0].get_next_product_id()
        if self.temp_storage.has_product(product_id):
            self.temp_storage.pop_product(product_id)
            return True
        else:
            return False
