from pyoccad.doc import add, get
from pyoccad.doc.create import makeDoc
from pyoccad.tests import testcase


class TestDocUtils(testcase.TestCase):

    def test_findByName(self):
        from pyoccad.create import CreateSolid

        myDoc = makeDoc()[0]
        sh_root = myDoc.Main().NewChild()
        box1 = CreateSolid.box_from_dims(1, 2, 3)
        add.shape(sh_root, box1, "sh1")

        lst = Doc_Utils.findByName(sh_root, "sh1")
        self.assertEqual(len(lst), 1)
        self.assertTrue(get.label_generated_shape(lst[0]).IsSame(box1))

        box2 = CreateSolid.box_from_dims(2, 2, 3)
        add.shape(sh_root, box2, "sh1")

        lst = Doc_Utils.findByName(sh_root, "sh1")
        self.assertEqual(len(lst), 2)
        self.assertTrue(get.label_generated_shape(lst[0]).IsSame(box1))
        self.assertTrue(get.label_generated_shape(lst[1]).IsSame(box2))

    def test_setShape(self):
        from pyoccad.create import CreateSolid

        myDoc = makeDoc()[0]
        sh_root = myDoc.Main().NewChild()
        box1 = CreateSolid.box_from_dims(1, 2, 3)
        add.shape(sh_root, box1, "box1")
        box2 = CreateSolid.box_from_dims(2, 2, 3)
        add.shape(sh_root, box2, "box2")

        self.assertTrue(get.label_generated_shape(Doc_Utils.findByName(sh_root, "box1")[0]).IsSame(box1))
        self.assertTrue(get.label_generated_shape(Doc_Utils.findByName(sh_root, "box2")[0]).IsSame(box2))

        box3 = CreateSolid.box_from_dims(2, 2, 2)
        Doc_Utils.setShape(sh_root, box3, "box3")

        self.assertEqual(sh_root.NbChildren(), 3)

        Doc_Utils.setShape(sh_root, box1, "box3")

        self.assertFalse(get.label_generated_shape(Doc_Utils.findByName(sh_root, "box3")[0]).IsSame(box3))
        self.assertTrue(get.label_generated_shape(Doc_Utils.findByName(sh_root, "box3")[0]).IsSame(box1))
        self.assertTrue(Doc_Utils.getLabelShapeOld(Doc_Utils.findByName(sh_root, "box3")[0]).IsSame(box3))
