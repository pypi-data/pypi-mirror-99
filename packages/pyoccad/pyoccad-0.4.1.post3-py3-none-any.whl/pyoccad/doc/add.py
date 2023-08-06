from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.TDataStd import TDataStd_Name
from OCC.Core.TDocStd import TDocStd_Document


class Add():

    @staticmethod
    def name(label, name, withUndo=False):
        doc = TDocStd_Document.Get(label);
        if withUndo: doc.OpenCommand()

        name_ExtendedString = TCollection_ExtendedString(name)
        TDataStd_Name.Set(label, name_ExtendedString)

        if withUndo: doc.CommitCommand()

    @staticmethod
    def label(label, name, withUndo=False):
        doc = TDocStd_Document.Get(label);
        if withUndo: doc.OpenCommand()

        ch = label.NewChild()
        name_ExtendedString = TCollection_ExtendedString(name)
        TDataStd_Name.Set(ch, name_ExtendedString)

        if withUndo: doc.CommitCommand()

        return ch

    @staticmethod
    def shape(label, sh, name="", withUndo=False):
        return Doc_Utils.addShape(label, sh, name, withUndo)

    @staticmethod
    def ax1(label, ax1, name="", withUndo=False):
        return Doc_Utils.addAx1(label, ax1, name, withUndo)

    @staticmethod
    def ax3(label, ax3, name="", withUndo=False):
        return Doc_Utils.addAx3(label, ax3, name, withUndo)

    @staticmethod
    def plane(label, pln, name="", withUndo=False):
        return Doc_Utils.addPlane(label, pln, name, withUndo)

    @staticmethod
    def line(label, lin, name="", withUndo=False):
        return Doc_Utils.addLine(label, lin, name, withUndo)

    @staticmethod
    def real(label, f, name="", withUndo=False):
        return Doc_Utils.addReal(label, f, name, withUndo)

    @staticmethod
    def point(label, p, name="", withUndo=False):
        return Doc_Utils.addPoint(label, p, name, withUndo)
