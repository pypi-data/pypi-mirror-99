from .iterable import iterable
from .instance import instance


def list_(v, class_or_tuple=None):
    if (
        class_or_tuple and
        isinstance(v, class_or_tuple)
    ):
        return [v]
    ret = list(iterable(v))
    if class_or_tuple:
        for i in ret:
            instance(i, class_or_tuple)
    return ret
