"""[summary]
"""
from vending_machine.juice import Juice


class JuiceSupplier:
    """[summary]"""

    def __init__(self, name2price: dict):
        """[summary]

        Args:
            name2price (dict): [description]
        """
        self.name2price = name2price

    def __call__(self, name: str):
        """[summary]

        Args:
            name (str): [description]

        Returns:
            [type]: [description]
        """
        # NOTE: Juice.price を削って、priceはJuiceSupplierだけで管理する？
        return Juice(name=name, price=self.name2price[name])
