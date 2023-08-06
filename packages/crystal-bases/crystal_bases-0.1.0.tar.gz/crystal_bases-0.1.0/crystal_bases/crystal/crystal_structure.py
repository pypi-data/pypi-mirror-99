from typing import Union, List, Dict
import crystal_bases.young.tableau as tableau
from typing import Any
import copy


def wt(tab: tableau.Tableau) -> list:
    """weight function

    Args:
        tab: tableau.Tableau [description]

    Returns:
        list: [description]

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> wt(tab)
        [2, 2, 0]
    """
    return Wt().wt(tab=tab)


def f(i: int) -> Any:
    """lowering operator f

    Args:
        i: int

    Returns:
        tableau.Tableau: [description]

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> f(i=1)(tab) # return None

        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> f(i=2)(tab).box()
        [[1, 1], [2, 3]]
    """

    def _f(tab: tableau.Tableau) -> Union[tableau.Tableau, None]:
        return F().f(i=i, tab=tab)

    return _f


def e(i: int) -> Any:
    """raiging operator e

    Args:
        i: int

    Returns:
        tableau.Tableau: [description]

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 3]], orientation='row')
        >>> e(i=1)(tab)

        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 3]], orientation='row')
        >>> e(i=2)(tab).box()
        [[1, 1], [2, 2]]
    """

    def _e(tab: tableau.Tableau) -> Union[str, None]:
        return E().e(i=i, tab=tab)

    return _e


def phi(i: int) -> Any:
    """phi

    Args:
        i: int

    Returns:
        int: [description]

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> phi(i=1)(tab)
        0

        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 2]], orientation='row')
        >>> phi(i=2)(tab)
        2
    """

    def _phi(tab: tableau.Tableau) -> str:
        return Phi().phi(i=i, tab=tab)

    return _phi


def epsilon(i: int) -> Any:
    """phi

    Args:
        i: int

    Returns:
        int: [description]

    Examples:
        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 3]], orientation='row')
        >>> epsilon(i=1)(tab)
        0

        >>> tab = tableau.tableau(boxes=[[1, 1], [2, 3]], orientation='row')
        >>> epsilon(i=2)(tab)
        1
    """

    def _epsilon(tab: tableau.Tableau) -> Union[tableau.Tableau, None]:
        return Epsilon().epsilon(i=i, tab=tab)

    return _epsilon


class Wt:
    def wt(self, tab: tableau.Tableau) -> list:
        return tab.weight()


class F:
    def f(self, i: int, tab: tableau.Tableau) -> tableau.Tableau:
        reading: List[Dict[str, Union[int, None]]] = SignatureRule().get_reading(
            tab=tab, reading="far_eastern"
        )
        signature: List[Dict[str, Union[int, None]]] = SignatureRule().get_signature(
            reading=reading, i=i
        )
        result: Dict[
            str, Union[Dict[str, Union[int, None]], int, None]
        ] = SignatureRule().signature_rule(signature=signature, i=i)
        act_point: Dict[str, Union[int, None]] = result["act_point_f"]
        if (act_point["row"] is None) & (act_point["col"] is None):
            return None
        else:
            boxes = copy.deepcopy(tab.box())
            boxes[act_point["row"]][act_point["col"]] = i + 1
            return tableau.tableau(boxes=boxes, orientation="row")


class E:
    def e(self, i: int, tab: tableau.Tableau) -> tableau.Tableau:
        reading: List[Dict[str, Union[int, None]]] = SignatureRule().get_reading(
            tab=tab, reading="far_eastern"
        )
        signature: List[Dict[str, Union[int, None]]] = SignatureRule().get_signature(
            reading=reading, i=i
        )
        result: Dict[
            str, Union[Dict[str, Union[int, None]], int, None]
        ] = SignatureRule().signature_rule(signature=signature, i=i)
        act_point: Dict[str, Union[int, None]] = result["act_point_e"]
        if (act_point["row"] is None) & (act_point["col"] is None):
            return None
        else:
            boxes = copy.deepcopy(tab.box())
            boxes[act_point["row"]][act_point["col"]] = i
            return tableau.Tableau(boxes=boxes, orientation="row")


class Phi:
    def phi(self, i: int, tab: tableau.Tableau) -> tableau.Tableau:
        reading = SignatureRule().get_reading(tab=tab, reading="far_eastern")
        signature = SignatureRule().get_signature(reading=reading, i=i)
        result = SignatureRule().signature_rule(signature=signature, i=i)
        return result["i"]


class Epsilon:
    def epsilon(self, i: int, tab: tableau.Tableau) -> tableau.Tableau:
        reading = SignatureRule().get_reading(tab=tab, reading="far_eastern")
        signature = SignatureRule().get_signature(reading=reading, i=i)
        result = SignatureRule().signature_rule(signature=signature, i=i)
        return result["i+1"]


class SignatureRule:
    def get_reading(
        self, tab: tableau.Tableau, reading="far_eastern"
    ) -> List[Dict[str, Union[int, None]]]:
        reading = []
        boxes = copy.deepcopy(tab.box())
        for row_num, row in enumerate(boxes):
            for col_num_re, box in enumerate(row[::-1]):
                reading = reading + [
                    {
                        "row": row_num,
                        "col": len(row) - col_num_re - 1,
                        "word": box,
                    }
                ]

        return reading

    def get_signature(
        self, reading: List[Dict[str, Union[int, None]]], i: int
    ) -> List[Dict[str, Union[int, None]]]:
        signature = [
            box
            if (box["word"] == i) or (box["word"] == i + 1)
            else {"row": box["row"], "col": box["col"], "word": None}
            for box in reading
        ]
        return signature

    def signature_rule(
        self, signature: List[Dict[str, Union[int, None]]], i: int
    ) -> Dict[str, Union[Dict[str, Union[int, None]], int, None]]:
        plus: int = 0
        minus: int = 0
        act_point_e: Dict[str, Union[int, None]] = {"row": None, "col": None}
        for box in signature:
            if box["word"] == i:
                plus = plus + 1
                if plus == 1:
                    act_point_f = {"row": box["row"], "col": box["col"]}
            if box["word"] == i + 1:
                if plus > 0:
                    plus = plus - 1
                    if plus == 0:
                        act_point_f = {"row": None, "col": None}
                elif plus == 0:
                    minus = minus + 1
                    act_point_e = {"row": box["row"], "col": box["col"]}
                    act_point_f = {"row": None, "col": None}

        return {
            "act_point_f": act_point_f,
            "act_point_e": act_point_e,
            "i": plus,
            "i+1": minus,
        }
