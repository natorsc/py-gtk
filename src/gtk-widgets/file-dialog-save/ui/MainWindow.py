# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')

from gi.repository import Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
BLP_FILE = BASE_DIR / 'MainWindow.blp'
UI_FILE = BASE_DIR / 'MainWindow.ui'

sys.path.append(str(BASE_DIR.parent.parent.parent / 'scripts'))

from blp import blp_to_ui

blp_to_ui(file=BLP_FILE)


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    gio_list_store = Gtk.Template.Child(name='gio_list_store')

    filter_all_files = Gtk.Template.Child(name='filter_all_files')
    filter_py_files = Gtk.Template.Child(name='filter_py_files')
    filter_txt_files = Gtk.Template.Child(name='filter_txt_files')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gio_list_store.append(item=self.filter_all_files)
        self.gio_list_store.append(item=self.filter_py_files)
        self.gio_list_store.append(item=self.filter_txt_files)

    @Gtk.Template.Callback()
    def on_button_save_clicked(self, widget):
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title(title='Save')
        file_dialog.set_initial_name(name='file-name')
        file_dialog.set_modal(modal=True)
        file_dialog.set_filters(filters=self.gio_list_store)
        file_dialog.save(parent=self, callback=self.on_file_dialog_dismissed)

    def on_file_dialog_dismissed(self, file_dialog, gio_task):
        local_file = file_dialog.save_finish(gio_task)
        print(f'File name: {local_file.get_basename()}')
        print(f'File path: {local_file.get_path()}')
        print(f'File URI: {local_file.get_uri()}\n')


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
