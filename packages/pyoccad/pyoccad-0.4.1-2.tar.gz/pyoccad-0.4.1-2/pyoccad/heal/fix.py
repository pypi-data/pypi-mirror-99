from OCC.Core.ShapeFix import ShapeFix_ShapeTolerance


def def_shape_tol(sh, tol):
    """Set shape tolerance
    
    Arguments:
        sh {TopoDS_Shape]} -- the shape to update
        tol {float} -- new shape's tolerance
    """
    ShapeFix_ShapeTolerance().SetTolerance(sh, tol)
