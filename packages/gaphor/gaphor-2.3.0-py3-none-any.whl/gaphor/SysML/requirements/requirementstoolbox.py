"""The definition for the requirements section of the toolbox."""

from gaphas.item import SE

from gaphor.core import gettext
from gaphor.diagram.diagramtoolbox import ToolDef, ToolSection, namespace_config
from gaphor.diagram.diagramtools import new_item_factory
from gaphor.SysML import diagramitems as sysml_items
from gaphor.SysML import sysml

requirements = ToolSection(
    gettext("Requirements"),
    (
        ToolDef(
            "toolbox-requirement",
            gettext("Requirement"),
            "gaphor-requirement-symbolic",
            "r",
            new_item_factory(
                sysml_items.RequirementItem,
                sysml.Requirement,
                config_func=namespace_config,
            ),
            handle_index=SE,
        ),
        ToolDef(
            "toolbox-satisfy-dependency",
            gettext("Satisfy"),
            "gaphor-satisfy-symbolic",
            "<Shift>I",
            new_item_factory(sysml_items.SatisfyItem),
        ),
        ToolDef(
            "toolbox-derive-reqt-dependency",
            gettext("Derive Reqt"),
            "gaphor-derive-symbolic",
            "<Shift>D",
            new_item_factory(sysml_items.DeriveReqtItem),
        ),
        ToolDef(
            "toolbox-trace-dependency",
            gettext("Trace"),
            "gaphor-trace-symbolic",
            "<Shift>E",
            new_item_factory(sysml_items.TraceItem),
        ),
        ToolDef(
            "toolbox-refine-dependency",
            gettext("Refine"),
            "gaphor-refine-symbolic",
            "<Shift>N",
            new_item_factory(sysml_items.RefineItem),
        ),
        ToolDef(
            "toolbox-verify-dependency",
            gettext("Verify"),
            "gaphor-verify-symbolic",
            "<Shift>V",
            new_item_factory(sysml_items.VerifyItem),
        ),
    ),
)
