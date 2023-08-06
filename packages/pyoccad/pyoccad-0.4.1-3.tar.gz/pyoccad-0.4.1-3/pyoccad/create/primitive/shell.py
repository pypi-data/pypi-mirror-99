from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shell


class CreateShell:

    @staticmethod
    def from_faces(f_lst):
        """Builds a shell from face list

        Parameters
        ----------
        f_lst: [TopoDS_Face]
            the faces

        Returns
        -------
        s : TopoDS_Shell

        """
        sh = TopoDS_Shell()
        aBuilder = BRep_Builder()
        aBuilder.MakeShell(sh)
        for f in f_lst:
            aBuilder.Add(sh, f)

        return sh
