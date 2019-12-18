from unittest import TestCase
from Truck import Truck


class TestTruck(TestCase):
    def test_pop_product(self):
        truck = Truck([5, 7, 0, 3], [3, 2, 4, 1])
        expected = [3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        for expect in expected:
            product_id = truck.pop_product()
            self.assertEqual(product_id, expect)

    def test_get_next_product_id(self):
        truck = Truck([5, 7, 0, 3], [3, 2, 4, 1])
        expected = [3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        for expect in expected:
            product_id = truck.get_next_product_id()
            self.assertEqual(product_id, expect)
            truck.pop_product()

    def test_is_empty(self):
        truck = Truck([5, 7, 0, 3], [3, 2, 4, 1])
        expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        self.assertEqual(truck.is_empty(), False)
        for expect in expected:
            truck.pop_product()
            is_empty = truck.is_empty()
            self.assertEqual(is_empty, expect)
