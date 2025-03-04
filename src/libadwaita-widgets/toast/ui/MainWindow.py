# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

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

    button = Gtk.Template.Child(name='button')
    toast = Gtk.Template.Child(name='toast')
    adw_toast_overlay = Gtk.Template.Child(name='adw_toast_overlay')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_button_clicked(self, button):
        button.set_sensitive(sensitive=False)
        self.adw_toast_overlay.add_toast(self.toast)

    @Gtk.Template.Callback()
    def on_toast_dismissed(self, toast):
        """Emitted when the toast has been dismissed."""
        print('[!] dismissed [!]')
        print('Emitted when the toast has been dismissed')
        self.button.set_sensitive(sensitive=True)

    @Gtk.Template.Callback()
    def on_toast_button_clicked(self, toast):
        """Emitted after the button has been clicked."""
        print('[!] button-clicked [!]')
        print('Emitted after the button has been clicked.')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='nators.com.github.PyGtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
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

    def on_preferences_action(self, action, param):
        print('Action `app.preferences` was active.')

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
