from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Tableau:
    boxes: List[list] = field(init=True, repr=True, compare=False)
    orientation: str = field(init=True, repr=True, compare=False)

    def __eq__(self, other):
        return self.boxes == other.boxes

    def shape(self) -> List[int]:
        return [len(row) for row in self.boxes]

    def weight(self) -> List[int]:
        weight: List[int] = []
        n = len(self.boxes) + 1  # the number of columns + 1
        for i in range(1, n + 1):
            count_i = 0
            for row in self.boxes:
                for box in row:
                    if box == i:
                        count_i = count_i + 1
            weight = weight + [count_i]

        return weight

    def box(self) -> List[list]:
        return self.boxes


def tableau(boxes: List[list], orientation="row") -> Tableau:
    """
    Generate Young tableau.

    Args:
        boxes: list
        orientation: str, optional
            Defaults to 'row'.

    Returns:
        list: [description]

    Examples:
    >>> tableau([[1, 2, 3], [2]]).box()
    [[1, 2, 3], [2]]

    >>> tableau([[1, 2, 3], [2]]).shape()
    [3, 1]

    >>> tableau([[1, 2, 3], [2]]).weight()
    [1, 2, 1]

    >>> tableau([[1, 2, 3], [2]]) == tableau([[1, 2, 3], [2]])
    True

    >>> tableau([[1, 2, 3], [2]]) == tableau([[1, 3, 3], [2]])
    False

    """
    return Tableau(boxes=boxes, orientation=orientation)
