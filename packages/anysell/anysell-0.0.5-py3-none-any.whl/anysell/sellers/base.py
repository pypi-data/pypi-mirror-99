import abc
from abc import ABC

from anysell.sellers.item import Item


class Seller(ABC):
    @abc.abstractmethod
    def create_post(self, item: Item):
        pass
