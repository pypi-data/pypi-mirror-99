from OCC.Core.XCAFApp import XCAFApp_Application
from OCC.Core.TDocStd import TDocStd_Document
from OCC.Core.XmlDrivers import xmldrivers
from OCC.Core.TCollection import TCollection_ExtendedString


def makeDoc(storageFormat="XmlOcaf"):
    app = XCAFApp_Application.GetApplication()
    xmldrivers.DefineFormat(app)
    storageFormat_ExtendedString = TCollection_ExtendedString(storageFormat)
    doc = TDocStd_Document(storageFormat_ExtendedString)
    app.NewDocument(storageFormat_ExtendedString, doc)
    return doc, app


def closeDoc(doc):
    doc.BeforeClose()
    doc.Close()


def makeDocFromFile(fileName, storageFormat="XmlOcaf"):
    doc, app = makeDoc(storageFormat)
    status = app.Open(fileName, doc)
    return doc
