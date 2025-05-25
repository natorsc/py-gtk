# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')

from gi.repository import Gdk, Gio, GObject, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
BLP_FILE = BASE_DIR / 'MainWindow.blp'
UI_FILE = BASE_DIR / 'MainWindow.ui'

sys.path.append(str(BASE_DIR.parent.parent.parent / 'scripts'))

from blp import blp_to_ui

blp_to_ui(file=BLP_FILE)


class DraggableRow(Gtk.ListBoxRow):
    def __init__(self, label_text):
        super().__init__()
        self.label_text = label_text

        # Row content.
        label = Gtk.Label(label=label_text)
        label.set_margin_top(margin=12)
        label.set_margin_end(margin=12)
        label.set_margin_bottom(margin=12)
        label.set_margin_start(margin=12)
        label.set_xalign(xalign=0)
        self.set_child(child=label)

        # 1. Drag source controller.
        drag_source = Gtk.DragSource.new()
        drag_source.set_actions(actions=Gdk.DragAction.MOVE)
        # When preparing the drag, we define what will be dragged.
        drag_source.connect('prepare', self.on_drag_source_prepare)
        # Add visual feedback when starting and ending the drag.
        drag_source.connect('drag-begin', self.on_drag_source_begin)
        drag_source.connect('drag-end', self.on_drag_source_end)
        self.add_controller(controller=drag_source)

        # 2. Drop target controller
        # GObject.TYPE_STRING is the GObject type for Python str.
        drop_target = Gtk.DropTarget.new(
            type=GObject.TYPE_STRING,
            actions=Gdk.DragAction.MOVE,
        )
        # Connect the 'drop' signal that will be emitted when an item is dropped over this row.
        drop_target.connect('drop', self.on_drop_target_drop)
        # Add visual feedback when a dragged item enters/leaves this row's area.
        drop_target.connect('enter', self.on_drop_target_enter)
        drop_target.connect('leave', self.on_drop_target_leave)
        self.add_controller(controller=drop_target)

    def on_drag_source_prepare(self, drag_source, x, y):
        # Store a reference to the row being dragged at the application level,
        # to avoid searching by text in `on_drop`.
        # The Main Window (or App) will hold a global reference to this.
        app = Gtk.Application.get_default()
        # Just for safety
        if hasattr(app, 'dragged_row'):
            app.dragged_row = self

        # Return the content to be loaded in the drag (label text)
        # GTK 4 uses Gdk.ContentProvider to manage drag-and-drop data.
        print(f'[!] on_drag_prepare [!]')
        print(f'Preparing drag for: {self.label_text}')
        return Gdk.ContentProvider.new_for_value(value=self.label_text)

    def on_drag_source_begin(self, drag_source, drag):
        # Visual feedback: makes the dragged item semi-transparent.
        print(f'[!] on_drag_source_begin [!]')
        print(f'Drag started for: {self.label_text}')
        self.set_opacity(opacity=0.5)

    def on_drag_source_end(self, drag_source, drag, delete_data):
        # Visual feedback: restores the item's opacity.
        print(f'[!] on_drag_source_end [!]')
        print(f'Drag finished for: {self.label_text}')
        self.set_opacity(opacity=1.0)
        # Clear the reference to the dragged row.
        app = Gtk.Application.get_default()
        if hasattr(app, 'dragged_row'):
            app.dragged_row = None

    def on_drop_target_enter(self, drop_target, x, y):
        # Visual feedback: changes the background color of the target row.
        print(f'[!] on_drop_target_enter [!]')
        print(f'Dragging over: {self.label_text}')
        return Gdk.DragAction.MOVE

    def on_drop_target_leave(self, drop_target):
        # Visual feedback: removes the background color from the target row.
        print(f'[!] on_drop_target_leave [!]')
        print(f'Left: {self.label_text}')

    def on_drop_target_drop(self, drop_target, value, x, y):
        # `value` is already the string we dragged (the source's label_text).
        print(f'[!] on_drop_target_drop [!]')
        dropped_text = value
        # Get the parent Gtk.ListBox.
        listbox = self.get_parent()

        # Retrieve the original row that was dragged.
        source_row = None
        # Try to get the reference to the dragged row that was stored in on_drag_prepare.
        app = Gtk.Application.get_default()
        if hasattr(app, 'dragged_row') and app.dragged_row is not None:
            source_row = app.dragged_row
            # Check if the text matches to ensure it's the right item.
            if source_row.label_text != dropped_text:
                # If it's not the same item, perhaps something was dragged from elsewhere or there was an error.
                print('[!] WARNING [!]')
                print(f"The dragged row's text ({source_row.label_text})")
                print(f'does not match the dropped text ({dropped_text}).')
                source_row = None  # Reset to avoid moving the wrong item

        # If the reference was not found or doesn't match (fallback to text search)
        if not source_row:
            print('[!] DEBUG [!]')
            print('on_drop - Searching for source_row by text (fallback)...')
            row_iter = listbox.get_first_child()
            while row_iter:
                if (
                    isinstance(row_iter, DraggableRow)
                    and row_iter.label_text == dropped_text
                ):
                    source_row = row_iter
                    break
                row_iter = row_iter.get_next_sibling()
        # Ensure we're not trying to drag onto the same row
        if source_row and source_row != self:
            print('[!] DEBUG [!]')
            print(f'on_drop - Dropped {source_row.label_text}')
            print(f'onto {self.label_text}')
            # Remove the row from its original position

            listbox.remove(child=source_row)
            # Determine the target index (where 'self' is currently located)
            # The new position will be before or after 'self'
            # (self.get_index() will give the index of 'self' after source_row has been removed)
            target_index = self.get_index()
            print('[!] DEBUG [!]')
            print(f'on_drop - Removed {source_row.label_text}. ')
            print(f'New target position: {target_index}')
            # Insert the row at the new position
            listbox.insert(
                child=source_row,
                position=target_index,
            )
            print('[!] DEBUG [!]')
            print(f'on_drop - {source_row.label_text} ')
            print(f'moved to index {target_index}.')
        else:
            print('[!] DEBUG [!]')
            print(f'DEBUG: on_drop - Could not move. ')
            print(f'source_row: {source_row}, target_row: {self}')
        # Indicate that the drop was handled
        return True


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    list_box = Gtk.Template.Child(name='list_box')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        for i in range(1, 6):
            self.list_box.append(child=DraggableRow(f'Item {i}'))


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Action `app.preferences` was active.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'app.{name}',
                accels=shortcuts,
            )


if __name__ == '__main__':
    app = ExampleApplication()
    app.run(sys.argv)
