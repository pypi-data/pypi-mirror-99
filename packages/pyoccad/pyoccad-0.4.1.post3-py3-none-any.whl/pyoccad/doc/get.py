from OCC.Core.TopAbs import TopAbs_COMPOUND, TopAbs_COMPSOLID, TopAbs_SOLID, TopAbs_SHELL, TopAbs_FACE, TopAbs_WIRE, \
    TopAbs_EDGE, TopAbs_VERTEX, TopAbs_SHAPE

from OCC.Core.TopoDS import topods

from pyoccad.doc import find


def label_name(label):
    return Doc_Utils.getLabelName(label)


def label_generated_shape(label):
    sh = Doc_Utils.getLabelShapeGenerated(label)
    if sh is None:
        return sh
    if sh.ShapeType() is TopAbs_SHAPE:
        return sh
    elif sh.ShapeType() is TopAbs_COMPOUND:
        return topods.Compound(sh)
    elif sh.ShapeType() is TopAbs_COMPSOLID:
        return topods.CompSolid(sh)
    elif sh.ShapeType() is TopAbs_SOLID:
        return topods.Solid(sh)
    elif sh.ShapeType() is TopAbs_SHELL:
        return topods.Shell(sh)
    elif sh.ShapeType() is TopAbs_FACE:
        return topods.Face(sh)
    elif sh.ShapeType() is TopAbs_WIRE:
        return topods.Wire(sh)
    elif sh.ShapeType() is TopAbs_EDGE:
        return topods.Edge(sh)
    elif sh.ShapeType() is TopAbs_VERTEX:
        return topods.Vertex(sh)


def label_generated_shapes(label, name):
    label_ls = find.all_label_by_name(label, name)
    sh_lst = []
    for label in label_ls:
        sh_lst.append(label_generated_shape(label))
    return sh_lst


def label_ax1(label):
    return Doc_Utils.getLabelAx1(label)


def ax1(label, name):
    L = find.label_by_name(label, name)
    return label_ax1(L)


def label_line(label):
    return Doc_Utils.getLabelLine(label)


def line(label, name):
    L = find.label_by_name(label, name)
    return label_line(L)


def label_plane(label):
    return Doc_Utils.getLabelPlane(label)


def plane(label, name):
    L = find.label_by_name(label, name)
    return label_plane(L)


def label_ax3(label):
    return Doc_Utils.getLabelAx3(label)


def ax3(label, name):
    L = find.label_by_name(label, name)
    return label_ax3(L)


def label_real(label):
    return Doc_Utils.getLabelReal(label)


def real(label, name):
    L = find.label_by_name(label, name)
    return label_real(L)


def label_point(label):
    return Doc_Utils.getLabelPoint(label)


def point(label, name):
    L = find.label_by_name(label, name)
    return label_point(L)
