from dataclasses import dataclass
from typing import List


@dataclass
class Item:
    category: str
    price: int
    title: str
    description: str
    filepaths: List[str]

    @classmethod
    def deserialize(cls, itemdict):
        return cls(
            category=itemdict["category"],
            price=int(itemdict["price"]) if itemdict["price"] else 0,
            title=itemdict["title"],
            description=itemdict["description"],
            filepaths=itemdict["filepaths"],  # todo - expand user? use cfg `img_path`?
        )
