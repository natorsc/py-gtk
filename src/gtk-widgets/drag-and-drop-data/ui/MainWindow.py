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


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    label = Gtk.Template.Child(name='label')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        drag_source = Gtk.DragSource.new()
        drag_source.set_actions(actions=Gdk.DragAction.COPY)
        drag_source.connect('prepare', self.on_drag_source_prepare)
        drag_source.connect('drag-begin', self.on_drag_source_begin)
        drag_source.connect('drag-end', self.on_drag_source_end)
        drag_source.connect('drag-cancel', self.on_drag_source_cancel)

        drop_target = Gtk.DropTarget.new(
            type=GObject.TYPE_STRING,
            actions=Gdk.DragAction.COPY,
        )
        drop_target.connect('drop', self.drop_target_drop)
        drop_target.connect('enter', self.drop_target_enter)
        drop_target.connect('leave', self.drop_target_leave)

        self.label.add_controller(drag_source)
        self.label.add_controller(drop_target)

    def on_drag_source_prepare(self, drop_target, x, y):
        print('[!] on_drag_source_prepare [!]')
        print(f'Widget = {drop_target}')
        print(f'Position on the x-axis = {x}')
        print(f'Position on the y-axis = {y}')

    def on_drag_source_begin(self):
        print('[!] on_drag_source_begin [!]')

    def on_drag_source_end(self):
        print('[!] on_drag_source_end [!]')

    def on_drag_source_cancel(self):
        print('[!] on_drag_source_cancel [!]')

    def drop_target_drop(self, drop_target, data, x, y):
        print('[!] drop_target_drop [!]')
        print(f'Widget = {drop_target}')
        print(f'Data = {data}')
        print(f'Position on the x-axis = {x}')
        print(f'Position on the y-axis = {y}')

    def drop_target_enter(self, drop_target, x, y):
        print('[!] drop_target_enter [!]')
        return True

    def drop_target_leave(self, drop_target):
        print('[!] drop_target_leave [!]')


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
