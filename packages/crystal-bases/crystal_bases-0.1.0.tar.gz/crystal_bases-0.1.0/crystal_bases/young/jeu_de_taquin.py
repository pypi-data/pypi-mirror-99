from typing import List, Dict, Any
import crystal_bases.young.tableau as tableau


def jeu_de_taquin(tab: tableau.Tableau) -> tableau.Tableau:
    """jeu de taquin

    Args:
        tableau: tableau.Tableau

    Returns:
        tableau.Tableau:

    Example
    >>> tab = tableau.Tableau(boxes=[[1, 1], [2, None]], orientation='row')
    >>> jeu_de_taquin(tab).box()
    [[None, 1], [1, 2]]

    >>> tab = tableau.Tableau(boxes=[[1, 2], [2, None]], orientation='row')
    >>> jeu_de_taquin(tab).box()
    [[None, 1], [2, 2]]

    >>> tab = tableau.Tableau(boxes=[[1, 2], [None, None]], orientation='row')
    >>> jeu_de_taquin(tab).box()
    [[None, None], [1, 2]]
    """
    return JeuDeTaquin().jeu_de_taquin(tab)


class JeuDeTaquin:
    def get_null_boxes(self, tab: tableau.Tableau) -> List[dict]:
        null_boxes: List[Dict[str, int]] = []
        boxes: List[list] = tab.box()
        for row_num, row in enumerate(boxes):
            for col_num, col in enumerate(row):
                if col is None:
                    null_boxes = null_boxes + [{"row": row_num, "col": col_num}]

        return null_boxes

    def move(self, tab: tableau.Tableau, box_pos: dict, orientation="back") -> Any:
        if orientation == "back":
            if (box_pos["row"] == 0) & (box_pos["col"] == 0):
                return tab
            else:
                result = self.backmove(tab, box_pos)
                return self.move(tab=result["tab"], box_pos=result["box_pos"])
        elif orientation == "forword":
            pass

    def backmove(
        self, tab: tableau.Tableau, box_pos: dict
    ) -> Dict[tableau.Tableau, dict]:
        boxes = tab.box()
        row_num = box_pos["row"]
        col_num = box_pos["col"]
        box = boxes[row_num][col_num]
        above = (
            boxes[row_num - 1][col_num] if row_num > 0 else 0
        )  # if box out of tab above = 0
        if above is None:
            above = 0

        left = (
            boxes[row_num][col_num - 1] if col_num > 0 else 0
        )  # if box out of tab above = 0
        if left is None:
            left = 0

        if (left == 0) and (above == 0):
            box_pos = {"row": 0, "col": 0}

        elif left > above:
            boxes[row_num][col_num], boxes[row_num][col_num - 1] = left, box
            box_pos = {"row": row_num, "col": col_num - 1}

        elif left <= above:
            boxes[row_num][col_num], boxes[row_num - 1][col_num] = above, box
            box_pos = {"row": row_num - 1, "col": col_num}

        return {
            "tab": tableau.Tableau(boxes=boxes, orientation="row"),
            "box_pos": box_pos,
        }

    def forwordmove(self):
        pass

    def jeu_de_taquin(self, tab: tableau.Tableau) -> tableau.Tableau:
        null_boxes = self.get_null_boxes(tab)
        for null_box in null_boxes:
            tab = self.move(tab, null_box)

        return tab
