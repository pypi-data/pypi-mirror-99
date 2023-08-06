import crystal_bases.young.tableau as tableau
from crystal_bases.young.jeu_de_taquin import jeu_de_taquin
from typing import Any
import copy


def pr(n: int) -> Any:
    """Schutzenberger's promotion operator

    Args:
        tab: tableau.Tableau

    Returns:
        tableau.Tableau:

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> pr(n = 3)(tab).box()
        [[2, 2], [3, 3]]

        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 3]], orientation='row')
        >>> pr(n = 3)(tab).box()
        [[1, 2], [2, 3]]
    """

    def _pr(
        tab: tableau.Tableau,
    ):
        return Pr().pr(tab=tab, n=n)

    return _pr


class Pr:
    def remove_ns(self, tab: tableau.Tableau, n: int) -> tableau.Tableau:
        boxes = copy.deepcopy(tab.box())
        for row_num, row in enumerate(boxes):
            for col_num, box in enumerate(row):
                if box == n:
                    boxes[row_num][col_num] = None

        return tableau.Tableau(boxes=boxes, orientation="row")

    def add_1s(self, tab: tableau.Tableau) -> tableau.Tableau:
        boxes = copy.deepcopy(tab.box())
        for row_num, row in enumerate(boxes):
            for col_num, box in enumerate(row):
                if box is not None:
                    boxes[row_num][col_num] = boxes[row_num][col_num] + 1

        return tableau.Tableau(boxes=boxes, orientation="row")

    def fill_nones(self, tab: tableau.Tableau) -> tableau.Tableau:
        boxes = copy.deepcopy(tab.box())
        for row_num, row in enumerate(boxes):
            for col_num, box in enumerate(row):
                if box is None:
                    boxes[row_num][col_num] = 1

        return tableau.Tableau(boxes=boxes, orientation="row")

    def jeu_de_taquin_move(self, tab: tableau.Tableau) -> tableau.Tableau:
        return jeu_de_taquin(tab)

    def pr(self, tab: tableau.Tableau, n: int) -> tableau.Tableau:
        tab = self.remove_ns(tab=tab, n=n)
        tab = self.jeu_de_taquin_move(tab=tab)
        tab = self.add_1s(tab=tab)
        tab = self.fill_nones(tab=tab)
        return tab
