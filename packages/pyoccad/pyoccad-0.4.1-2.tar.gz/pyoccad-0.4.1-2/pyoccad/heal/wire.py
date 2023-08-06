from OCC.Core.ShapeUpgrade import ShapeUpgrade_ShapeDivideContinuity
from OCC.Core.GeomAbs import GeomAbs_C2


def split_to_c2(w):
    ''' Heals a wire to C2
    DO NOT USE: untested

    Parameters
    ----------
    w : TopoDS_Wire
        the wire to be healed

    Returns 
    -------
    
    
    '''
    raise NotImplementedError

    ShapeDivideContinuity = ShapeUpgrade_ShapeDivideContinuity(w)
    ShapeDivideContinuity.SetPCurveCriterion(GeomAbs_C2)
    sh = ShapeDivideContinuity.Result()
    w_lists = subshapes.get_wires(sh)
    if len(w_lists) > 1:
        print("warning, several wires created, returning first one")
    elif len(w_lists) == 0:
        raise Exception

    return w_lists[0]
