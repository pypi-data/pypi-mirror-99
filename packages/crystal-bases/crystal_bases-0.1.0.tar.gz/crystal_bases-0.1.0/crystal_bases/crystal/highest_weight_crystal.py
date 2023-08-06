from dataclasses import dataclass, field
from typing import Union, List, Set
from crystal_bases.young.tableau import tableau, Tableau


@dataclass(frozen=True)
class HighestWeightCrystal:
    lie_type: str = field(init=True, repr=True, compare=False)
    n: str = field(init=True, repr=True, compare=False)
    highest_weight: list = field(init=True, repr=True, compare=False)

    def get_weights(self) -> List[list]:
        pass

    def realization(self) -> Set[Tableau]:
        return set()