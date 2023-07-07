from bitarray import bitarray
from typing import List
def list_intents_via_Lindig(itemsets: List[bitarray], attr_extents: List[bitarray]):

    class NotFound(Exception):
        pass

    def __down__(intent: List[bitarray], itemsets: List[bitarray]):
        if intent == []:
            return itemsets
        down = intent[0]
        for attr in intent[1:]:
            down = down & attr
        down =  [itemsets[i] for i in range(len(down)) if down[i] == 1]
        return down

    def __up__(extent: List[bitarray], attr_extents: List[bitarray]):
        if extent == []:
            return(attr_extents)
        up = extent[0]
        for obj in extent[1:]:
            up = up & obj
        up = [attr_extents[i] for i in range(len(up)) if up[i] == 1]
        return up

    def check_intersection(list1: List[bitarray], list2: List[bitarray]):
        has_intersection = False

        for bitarray1 in list1:
            for bitarray2 in list2:
                if bitarray1 == bitarray2:
                    has_intersection = True
                    break
        return has_intersection
    
    def compute_extent_bit(extent: List[bitarray], attr_extents: List[bitarray]):
        if extent == []:
            return(bitarray([1 for _ in range(len(attr_extents))]))
        bit_extent = extent[0]
        for obj in extent[1:]:
            bit_extent = bit_extent & obj
        return(bit_extent)
    
    def find_upper_neighbors(concept_extent: List[bitarray], itemsets: List[bitarray], attr_extents: List[bitarray]):
        min_set = [obj for obj in itemsets if obj not in concept_extent]
        neighbors = []

        for g in [obj for obj in itemsets if obj not in concept_extent]:
            B1 = __up__(concept_extent + [g], attr_extents)
            A1 = __down__(B1, itemsets)
            if not check_intersection(min_set, [obj for obj in A1 if obj not in concept_extent and obj not in [g]]):
                neighbors.append(A1)
            else:
                min_set.remove(g)
        return neighbors
    
    def find_next_concept_extent(concept_extent: List[bitarray], List_extents: List[bitarray], attr_extents: List[bitarray]):
        next_concept_extent = None
        for extent in List_extents:
            if compute_extent_bit(extent, attr_extents) < compute_extent_bit(concept_extent, attr_extents) and (next_concept_extent is None or compute_extent_bit(extent, attr_extents) > compute_extent_bit(next_concept_extent, attr_extents)):
                next_concept_extent = extent
        if next_concept_extent is not None:
            return next_concept_extent
        raise NotFound("Next concept not found in Lattice")

        
    Lattice_data_intents = []  # concepts set
    concept_extent = __down__(attr_extents, itemsets)  # Initial Concept
    Lattice_data_intents.append(concept_extent)  # Insert the initial concept into Lattice

    while True:
        for parent in find_upper_neighbors(concept_extent, itemsets, attr_extents):
            if parent not in Lattice_data_intents:
              Lattice_data_intents.append(parent)

        try:
            concept_extent = find_next_concept_extent(concept_extent, Lattice_data_intents)
        except NotFound:
            break
    return Lattice_data_intents
