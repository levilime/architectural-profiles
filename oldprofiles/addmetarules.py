from solving.util import dimension_order_with_negative, dimension_directions, merge_dicts, invert_dimension
from functools import reduce
import numpy as np


def retrieve_metapositions(indices):
    """
    indices correspond to block ids, deduces whether a block has a certain meta position.

    Metapositions are whether a block has a certain solution edge. So y means that the solution
    ends up from that block.
    :param indices: a set of block ids (tuple)
    """
    # TODO calculated the ordered indices but this is not used
    ordered_indices = dict(reduce(lambda agg, k: dict(agg, **{k: []}), dimension_order_with_negative, {}),
                           **{"middle": []})
    indices_dict = set()
    for index in indices:
        indices_dict.add(index)
    indices_metapositions = reduce(lambda agg, k: merge_dicts(agg, {k: []}), indices, {})
    for index in indices:
        for d in dimension_directions:
            if tuple(np.add(index, dimension_directions[d])) not in indices_dict:
                ordered_indices[d].append(index)
                indices_metapositions[index].append(d)
        if len(indices_metapositions[index]) < 1:
            ordered_indices["middle"].append(index)
            indices_metapositions[index].append("middle")
    return indices_metapositions
