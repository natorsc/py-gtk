# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent


@Gtk.Template(filename=str(BASE_DIR.joinpath('ShortcutsWindow.ui')))
class ShortcutsWindow(Gtk.ShortcutsWindow):
    __gtype_name__ = 'ShortcutsWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(filename=str(BASE_DIR.joinpath('MainWindow.ui')))
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action(
            'shortcuts-window',
            self.on_shortcuts_window_action,
            ['<primary>1'],
        )

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

    def on_shortcuts_window_action(self, action, param):
        shortcuts_window = ShortcutsWindow(
            transient_for=self.get_active_window()
        )
        shortcuts_window.present()

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
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
