"""The Toolbox which is the tool palette.

This is the toolbox in the lower left of the screen.
"""

import logging
from typing import Optional, Sequence, Tuple

from gi.repository import Gdk, GLib, Gtk

from gaphor.abc import ActionProvider
from gaphor.core import gettext
from gaphor.core.eventmanager import event_handler
from gaphor.diagram.diagramtoolbox import ToolDef
from gaphor.ui.abc import UIComponent
from gaphor.ui.event import ModelingLanguageChanged

log = logging.getLogger(__name__)


class Toolbox(UIComponent, ActionProvider):

    TARGET_STRING = 0
    TARGET_TOOLBOX_ACTION = 1
    DND_TARGETS = [
        Gtk.TargetEntry.new("STRING", Gtk.TargetFlags.SAME_APP, TARGET_STRING),
        Gtk.TargetEntry.new("text/plain", Gtk.TargetFlags.SAME_APP, TARGET_STRING),
        Gtk.TargetEntry.new(
            "gaphor/toolbox-action", Gtk.TargetFlags.SAME_APP, TARGET_TOOLBOX_ACTION
        ),
    ]

    title = gettext("Toolbox")

    def __init__(self, event_manager, main_window, properties, modeling_language):
        self.event_manager = event_manager
        self.main_window = main_window
        self.properties = properties
        self.modeling_language = modeling_language
        self._toolbox: Optional[Gtk.ToolPalette] = None
        self._toolbox_container: Optional[Gtk.ScrolledWindow] = None

    def open(self) -> Gtk.ScrolledWindow:
        toolbox = self.create_toolbox(self.modeling_language.toolbox_definition)
        toolbox_container = self.create_toolbox_container(toolbox)
        self.event_manager.subscribe(self._on_modeling_language_changed)
        self._toolbox = toolbox
        self._toolbox_container = toolbox_container
        return toolbox_container

    def close(self):
        if self._toolbox:
            self._toolbox.destroy()
            self._toolbox = None
        self.event_manager.unsubscribe(self._on_modeling_language_changed)

    def create_toolbox_button(
        self, action_name: str, icon_name: str, label: str, shortcut: Optional[str]
    ) -> Gtk.ToggleToolButton:
        """Creates a tool button for the toolbox.

        Args:
            action_name (str): The action for the button.
            icon_name (str): The button icon.
            label (str): The label for the button.
            shortcut (str): The optional button shortcut.

        Returns: The Gtk.ToggleToolButton.
        """
        button = Gtk.ToggleToolButton.new()
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.BUTTON)
        button.set_icon_widget(icon)
        button.set_action_name("diagram.select-tool")
        button.set_action_target_value(GLib.Variant.new_string(action_name))
        if label:
            if shortcut:
                a, m = Gtk.accelerator_parse(shortcut)
                button.set_tooltip_text(f"{label} ({Gtk.accelerator_get_label(a, m)})")
            else:
                button.set_tooltip_text(f"{label}")

        # Enable Drag and Drop
        if action_name != "toolbox-pointer":
            inner_button = button.get_children()[0]
            inner_button.drag_source_set(
                Gdk.ModifierType.BUTTON1_MASK | Gdk.ModifierType.BUTTON3_MASK,
                self.DND_TARGETS,
                Gdk.DragAction.COPY | Gdk.DragAction.LINK,
            )
            inner_button.drag_source_set_icon_name(icon_name)
            inner_button.connect(
                "drag-data-get", self._button_drag_data_get, action_name
            )

        return button

    def create_toolbox(
        self, toolbox_actions: Sequence[Tuple[str, Sequence[ToolDef]]]
    ) -> Gtk.ToolPalette:
        """Create the Gtk.ToolPalette for the toolbox."""

        toolbox = Gtk.ToolPalette.new()
        toolbox.connect("destroy", self._on_toolbox_destroyed)

        collapsed = self.properties.get("toolbox-collapsed", {})

        def on_collapsed(widget, prop, index):
            collapsed[index] = widget.get_property("collapsed")
            self.properties.set("toolbox-collapsed", collapsed)

        for index, (title, items) in enumerate(toolbox_actions):
            tool_item_group = Gtk.ToolItemGroup.new(title)
            tool_item_group.set_property("collapsed", collapsed.get(index, False))
            tool_item_group.connect("notify::collapsed", on_collapsed, index)
            for action_name, label, icon_name, shortcut, *rest in items:
                button = self.create_toolbox_button(
                    action_name, icon_name, label, shortcut
                )
                tool_item_group.insert(button, -1)
                button.show_all()

            toolbox.add(tool_item_group)
            tool_item_group.show()

        toolbox.show()
        return toolbox

    def create_toolbox_container(self, toolbox: Gtk.ToolPalette) -> Gtk.ScrolledWindow:
        """Create a toolbox container.

        Args:
            toolbox: The Gtk.ToolPalette to add.

        Returns: The Gtk.ScrolledWindow.
        """
        toolbox_container = Gtk.ScrolledWindow()
        toolbox_container.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        toolbox_container.add(toolbox)
        toolbox_container.show()
        return toolbox_container

    @event_handler(ModelingLanguageChanged)
    def _on_modeling_language_changed(self, event) -> None:
        """Reconfigures the toolbox based on the modeling language selected.

        Args:
            event: The ModelingLanguageChanged event.
        """
        toolbox = self.create_toolbox(self.modeling_language.toolbox_definition)
        if self._toolbox_container:
            self._toolbox_container.remove(self._toolbox_container.get_child())
            self._toolbox_container.add(toolbox)
        self._toolbox = toolbox

    def _on_toolbox_destroyed(self, widget):
        self._toolbox = None

    def _button_drag_data_get(self, button, context, data, info, time, action_name):
        """The drag-data-get event signal handler.

        The drag-data-get signal is emitted on the drag source when the drop
        site requests the data which is dragged.

        Args:
            button (Gtk.Button): The button that received the signal.
            context (Gdk.DragContext): The drag context.
            data (Gtk.SelectionData): The data to be filled with the dragged
                data.
            info (int): The info that has been registered with the target in
                the Gtk.TargetList
            time (int): The timestamp at which the data was received.
        """
        data.set(type=data.get_target(), format=8, data=action_name.encode())
