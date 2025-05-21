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
DIALOG = str(BASE_DIR.joinpath('AdwMessageDialog.ui'))


@Gtk.Template(filename=DIALOG)
class MessageDialog(Adw.MessageDialog):
    __gtype_name__ = 'MessageDialog'

    def __init__(self, **kwargs):
        super(MessageDialog, self).__init__(**kwargs)

    @Gtk.Template.Callback()
    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK.value_nick:
            print('OK button pressed')
        elif response == Gtk.ResponseType.CANCEL.value_nick:
            print('CANCEL button pressed')


@Gtk.Template(filename=UI)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super(ExampleWindow, self).__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_button_clicked(self, button):
        dialog = MessageDialog(transient_for=self)
        dialog.present()


class ExampleApplication(Adw.Application):
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
