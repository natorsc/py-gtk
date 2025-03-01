# -*- coding: utf-8 -*-
"""Python and GTK: PyGObject Gtk.ListBox() Adw.ComboRow().

blueprint-compiler: `error: unsupported XML tag: <items>`.
"""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

BASE_DIR = pathlib.Path(__file__).resolve().parent
UI = BASE_DIR / 'MainWindow.ui'


@Gtk.Template(filename=UI)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_adw_combo_row_selected(self, comborow, GParamUInt):
        print(f'Position of the selected item {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Text of the selected item {selected_item.get_string()}')

    @Gtk.Template.Callback()
    def on_adw_combo_row_selected_item(self, comborow, GParamObject):
        print(f'Position of the selected item {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Text of the selected item {selected_item.get_string()}')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
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
