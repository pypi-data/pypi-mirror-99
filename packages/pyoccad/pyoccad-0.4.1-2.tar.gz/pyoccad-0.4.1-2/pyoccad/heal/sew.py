from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Sewing


def to_compound(sh_lst, tol=1e-6):
    """Sew the shapes  with given tolerance
    
    Parameters
    ----------
    sh_lst :  {container of TopoDS_Shape}        

    Raises
    ------
    RimtimeError
        if something goes wrong with occ
    
    Returns
    -------
    TopoDS_Shape, the sewed shape
    
    """
    Sewing = BRepBuilderAPI_Sewing(tol)
    for sh in sh_lst:
        Sewing.Add(sh)

    Sewing.Perform()
    return Sewing.SewedShape()


def to_shells(sh_lst, tol=1e-6):
    """Sew the shapes  with given tolerance to build shells

    Parameters
    ----------
    sh_lst :  {container of TopoDS_Shape}
        the shell list to sew

    Raises
    ------
    RimtimeError
        if something goes wrong with occ

    Returns
    -------
    s : {TopoDS_Shell}
        list of sewed shells

    """
    from pyoccad.explore import ExploreSubshapes

    return ExploreSubshapes.get_shells(to_compound(sh_lst, tol))
