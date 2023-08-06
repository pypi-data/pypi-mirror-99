from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.TDocStd import TDocStd_Document


def name(label, name, withUndo=False):
    """Add name attibute to label

    Arguments:
        label {TDF_Label} -- label to update
        name {str} -- label name to set

    Keyword Arguments:
        withUndo {bool} -- use undo/redo mechanism (default: {False})
    """
    doc = TDocStd_Document.Get(label)
    if withUndo:
        doc.OpenCommand()

    name_ExtendedString = TCollection_ExtendedString(name)
    TDataStd_Name.Set(label, name_ExtendedString)

    if withUndo:
        doc.CommitCommand()


def shape(label, sh, name="", withUndo=False, recursiveSearch=False):
    """Add TopoDS_Shape attibute to label if name is provided, and exist in child list 
    label's shape will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        sh {TopoDS_Shape} -- shape to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setShape(label, sh, name, withUndo)


def ax1(label, ax1, name="", withUndo=False, recursiveSearch=False):
    """Add gp_Ax1 attibute to label if name is provided, and exist in child list 
    label's ax will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        ax1 {gp_Ax1} -- axis to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """

    return Doc_Utils.setAx1(label, ax1, name, withUndo)


def ax3(label, ax3, name="", withUndo=False, recursiveSearch=False):
    """Add gp_Ax3 attibute to label if name is provided, and exist in child list 
    label's ax will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        ax3 {gp_Ax3} -- axis to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setAx3(label, ax3, name, withUndo)


def plane(label, pln, name="", withUndo=False, recursiveSearch=False):
    """Add gp_Pln attibute to label if name is provided, and exist in child list 
    label's plane will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        pln {gp_Pln} -- Plane to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setPlane(label, pln, name, withUndo)


def line(label, lin, name="", withUndo=False, recursiveSearch=False):
    """Add gp_Lin attibute to label if name is provided, and exist in child list 
    label's line will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        lin {gp_Lin} -- Line to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setLine(label, lin, name, withUndo)


def real(label, f, name="", withUndo=False, recursiveSearch=False):
    """Add real attibute to label if name is provided, and exist in child list 
    label's real will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        f {float} -- real to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setReal(label, f, name, withUndo)


def point(label, p, name="", withUndo=False, recursiveSearch=False):
    """Add gp_Point attibute to label if name is provided, and exist in child list 
    label's point will be updated
    
    Arguments:
        label {TDF_Label} -- label to update
        p {gp_Pnt} -- PointT to store
    
    Keyword Arguments:
        name {str} -- Shape name (default: {""})
        withUndo {bool} -- use undo/redo mechanism (default: {False})
        recursiveSearch {bool} -- Toggle recursive search in children lists (default: {False})
    """
    return Doc_Utils.setPoint(label, p, name, withUndo)
