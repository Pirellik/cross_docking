class Truck:
    def __init__(self, products, product_priorities):
        self.product_list = sorted(zip(range(0, len(product_priorities)), products, product_priorities), key=lambda x: x[2])
        self.product_list = [[x[0], x[1]] for x in self.product_list]
        assert(sum([x[1] for x in self.product_list]))
        self.product_list = list(filter(lambda x: x[1], self.product_list))
        for elem in self.product_list:
            assert(elem[1])

    def pop_product(self):
        if not self.product_list:
            return -1

        self.product_list[0][1] -= 1

        product_id = self.product_list[0][0]

        if not self.product_list[0][1]:
            self.product_list.pop(0)

        return product_id

    def get_next_product_id(self):
        if self.product_list:
            return self.product_list[0][0]
        else:
            return -1

    def is_empty(self):
        return not sum([x[1] for x in self.product_list])


# truck = Truck([5,7, 0, 3], [3,2, 4, 1])
# while not truck.is_empty():
#     print(truck.get_next_product_id())
#     truck.pop_product()
#     print(truck.product_list)
