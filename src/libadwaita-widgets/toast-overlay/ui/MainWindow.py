# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent.parent.parent / 'scripts'))

from blp import blp_to_ui

UI_FILE = BASE_DIR / 'MainWindow.ui'
BLP_FILE = BASE_DIR / 'MainWindow.blp'
blp_to_ui(file=BLP_FILE)


Adw.init()


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    button = Gtk.Template.Child(name='button')
    adw_toast_overlay = Gtk.Template.Child(name='adw_toast_overlay')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_button_clicked(self, button):
        toast = Adw.Toast.new(title='Lorem Ipsum')
        toast.set_button_label(button_label='Undo')
        toast.set_action_name(action_name='app.toast')
        toast.connect('dismissed', self.on_toast_dismissed)
        toast.connect('button-clicked', self.on_toast_button_clicked)
        self.adw_toast_overlay.add_toast(toast)

    def on_toast_dismissed(self, toast):
        print('[!] on_toast_dismissed [!]')

    def on_toast_button_clicked(self, toast):
        print('[!] on_toast_button_clicked [!]')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])

        self.create_action('toast', self.on_toast_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_toast_action(self, action, param):
        """It will be activated when clicking the button."""
        print('[!] action-name [!]')
        print('Action `app.toast` was active.')
        print('It will be activated when clicking the button')

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
