class TemporaryStorage:
    def __init__(self, num_product_types):
        self.products = [0] * num_product_types

    def add_product(self, product_id):
        self.products[product_id] += 1

    def has_product(self, product_id):
        return bool(self.products[product_id])

    def pop_product(self, product_id):
        self.products[product_id] -= 1


