"""Profile Import dependency relationship."""

from gaphor import UML
from gaphor.diagram.presentation import LinePresentation
from gaphor.diagram.shapes import Text, draw_arrow_head
from gaphor.diagram.support import represents
from gaphor.UML.modelfactory import stereotypes_str


@represents(UML.PackageImport)
class PackageImportItem(LinePresentation):
    """Profile Import dependency relationship."""

    def __init__(self, diagram, id=None):
        super().__init__(diagram, id, style={"dash-style": (7.0, 5.0)})

        self.shape_middle = Text(
            text=lambda: stereotypes_str(self.subject, ("import",)),
        )
        self.watch("subject.appliedStereotype.classifier.name")
        self.draw_head = draw_arrow_head
