# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
UI = BASE_DIR / 'MainWindow.ui'


Adw.init()


@Gtk.Template(filename=UI)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
            flags=Gio.ApplicationFlags.FLAGS_NONE,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('about', self.on_about_action)

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

    def on_about_action(self, action, param):
        dialog = Adw.AboutWindow.new()
        dialog.set_transient_for(parent=self.get_active_window())
        dialog.set_application_name('Python e GTK')
        dialog.set_version('0.0.1')
        dialog.set_developer_name('Renato Cruz (natorsc)')
        dialog.set_license_type(Gtk.License(Gtk.License.MIT_X11))
        dialog.set_comments(
            'Creating graphical interfaces with the Python programming '
            'language (PyGObject) and the GTK graphics toolkit'
        )
        dialog.set_website('https://gtk.justcode.com.br')
        dialog.set_issue_url(
            'https://github.com/natorsc/gui-python-pygobject-gtk/issues'
        )
        dialog.add_credit_section('Contributors', ['Name-01', 'Name-02'])
        dialog.set_translator_credits('Renato Cruz')
        dialog.set_copyright('© 2022 Renato Cruz (natorsc)')
        dialog.set_developers(['natorsc https://github.com/natorsc'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.present()

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
