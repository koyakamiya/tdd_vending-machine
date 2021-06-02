from vending_machine.juice import Juice


class JuiceSupplier:
    def __init__(self, name2price: dict):
        self.name2price = name2price

    def __call__(self, name: str):
        return Juice(name=name, price=self.name2price[name])
