import random
import json


class RandomProblemGenerator:
    def __init__(self, R, S, N, M, K, G, F, U, V, min_product_amount, max_product_amount):
        self.problem_instance = {
            'R': R,
            'S': S,
            'N': N,
            'M': M,
            'K': K,
            'G': G,
            'F': F,
            'U': U,
            'V': V,
            'a': [],
            'b': [],
            'c': [],
            'd': []
        }
        self.min_product_amount = min_product_amount
        self.max_product_amount = max_product_amount

    def randomize(self):
        products_amount = self._get_products_nums(self.problem_instance)
        self._fill_trucks(self.problem_instance, products_amount)
        self._fill_product_priorities(self.problem_instance, 'a', 'N')
        self._fill_product_priorities(self.problem_instance, 'c', 'M')

    def get_problem_instance(self):
        return self.problem_instance

    def read_json(self, filepath):
        with open(filepath) as json_file:
            self.problem_instance = json.load(json_file)

    def save_json(self, filepath):
        with open(filepath, 'w') as outfile:
            json.dump(self.problem_instance, outfile)

    def _get_products_nums(self, problem_instance):
        products_amount = []
        for _ in range(0, problem_instance['K']):
            products_amount.append(random.randint(self.min_product_amount, self.max_product_amount))
        return products_amount

    def _fill_trucks(self, problem_instance, available_products):
        self._fill_truck_type('b', 'N', problem_instance, available_products)
        self._fill_truck_type('d', 'M', problem_instance, available_products)

    @staticmethod
    def _fill_truck_type(truck_inventory_var, num_trucks_var, problem_instance, available_products):
        problem_instance[truck_inventory_var] = []
        for product_id in range(0, problem_instance['K']):
            problem_instance[truck_inventory_var].append([])
            total_amount = available_products[product_id]
            for truck_id in range(0, problem_instance[num_trucks_var]):
                amount_per_truck = random.randint(0, int(available_products[product_id] * 2 / problem_instance[num_trucks_var]))
                if amount_per_truck <= total_amount:
                    problem_instance[truck_inventory_var][product_id].append(amount_per_truck)
                    total_amount -= amount_per_truck
                elif total_amount:
                    problem_instance[truck_inventory_var][product_id].append(total_amount)
                    total_amount = 0
                else:
                    problem_instance[truck_inventory_var][product_id].append(0)

                if truck_id == problem_instance[num_trucks_var] - 1 and total_amount:
                    problem_instance[truck_inventory_var][product_id][truck_id] += total_amount

        problem_instance[truck_inventory_var] = [*zip(*problem_instance[truck_inventory_var])]

    @staticmethod
    def _fill_product_priorities(problem_instance, truck_prio_var, num_trucks_var):
        random.seed()
        problem_instance[truck_prio_var] = []
        for truck_id in range(0, problem_instance[num_trucks_var]):
            random_order = []
            for priority in range(1, problem_instance['K'] + 1):
                random_order.append((priority, random.random()))
            random_order = sorted(random_order, key=lambda x: x[1])
            problem_instance[truck_prio_var].append([x[0] for x in random_order])
