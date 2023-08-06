from OCC.Core.TCollection import TCollection_ExtendedString
from OCC.Core.IGESCAFControl import IGESCAFControl_Writer


def save(doc, app, file_name):
    app.SaveAs(doc, TCollection_ExtendedString(file_name))


def export_igs(doc, file_name):
    writer = IGESCAFControl_Writer()
    writer.Transfer(doc)
    writer.Write(file_name)
