from unittest import TestCase
from src.RandomProblemGenerator import RandomProblemGenerator
import json
import hashlib
from copy import copy


def hash_dict(d):
    return hashlib.sha1(json.dumps(d, sort_keys=True).encode('utf8')).hexdigest()


class TestRandomProblemGenerator(TestCase):
    def test_randomize(self):
        random_gen = RandomProblemGenerator(8, 7, 18, 21, 17, 1, 1, 1, 1, 80, 200)
        random_gen.randomize()

        problem_inst_1 = copy(random_gen.get_problem_instance())
        random_gen.randomize()
        problem_inst_2 = copy(random_gen.get_problem_instance())

        self.assertNotEqual(hash_dict(problem_inst_1), hash_dict(problem_inst_2))

    def test__get_products_nums(self):
        _min = 80
        _max = 200
        random_gen = RandomProblemGenerator(8, 7, 18, 21, 17, 1, 1, 1, 1, _min, _max)
        products_nums = random_gen._get_products_nums(random_gen.get_problem_instance())
        for num in products_nums:
            self.assertGreaterEqual(num, _min)
            self.assertLessEqual(num, _max)

    def test__fill_trucks(self):
        random_gen = RandomProblemGenerator(8, 7, 18, 21, 17, 1, 1, 1, 1, 80, 200)
        products_nums = random_gen._get_products_nums(random_gen.get_problem_instance())
        random_gen._fill_trucks(random_gen.get_problem_instance(), products_nums)
        problem_instance = random_gen.get_problem_instance()
        for inbound_product_nums, outbound_product_nums, prod_nums in zip(problem_instance['b'],
                                                                          problem_instance['d'],
                                                                          products_nums):
            self.assertEqual(sum(inbound_product_nums), sum(outbound_product_nums))

    def test__fill_truck_type(self):
        random_gen = RandomProblemGenerator(8, 7, 18, 21, 17, 1, 1, 1, 1, 80, 200)
        products_nums = random_gen._get_products_nums(random_gen.get_problem_instance())
        random_gen._fill_truck_type('b', 'N', random_gen.get_problem_instance(), products_nums)
        random_gen._fill_truck_type('d', 'M', random_gen.get_problem_instance(), products_nums)
        problem_instance = random_gen.get_problem_instance()
        for inbound_product_nums, outbound_product_nums, prod_nums in zip(problem_instance['b'],
                                                                          problem_instance['d'],
                                                                          products_nums):
            self.assertEqual(sum(outbound_product_nums), prod_nums)
            self.assertEqual(sum(inbound_product_nums), prod_nums)

    def test__fill_product_priorities(self):
        num_product_types = 17
        random_gen = RandomProblemGenerator(8, 7, 18, 21, num_product_types, 1, 1, 1, 1, 80, 200)
        random_gen._fill_product_priorities(random_gen.get_problem_instance(), 'a', 'N')
        random_gen._fill_product_priorities(random_gen.get_problem_instance(), 'c', 'M')

        problem_inst = random_gen.get_problem_instance()

        for truck_id in range(0, problem_inst['N']):
            for prio in range(1, num_product_types + 1):
                self.assertIn(prio, problem_inst['a'][truck_id])

        for truck_id in range(0, problem_inst['M']):
            for prio in range(1, num_product_types + 1):
                self.assertIn(prio, problem_inst['c'][truck_id])
