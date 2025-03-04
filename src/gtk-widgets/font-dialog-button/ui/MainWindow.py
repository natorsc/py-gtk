# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent


@Gtk.Template(filename=str(BASE_DIR.joinpath('MainWindow.ui')))
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @Gtk.Template.Callback()
    def on_font_selected(self, font_dialog_button, g_param_boxed):
        pango_font_description = font_dialog_button.get_font_desc()
        print(f'Font name: {pango_font_description.get_family()}')
        print(f'Font size: {pango_font_description.get_size()}')
        print(f'Font style: {pango_font_description.get_style()}')
        print(f'Font weight: {pango_font_description.get_weight()}')


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='nators.com.github.PyGtk',
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
