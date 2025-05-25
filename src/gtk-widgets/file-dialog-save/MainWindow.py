# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk

FILTER_ALL_FILES = Gtk.FileFilter()
FILTER_ALL_FILES.set_name(name='All')
FILTER_ALL_FILES.add_pattern(pattern='*')

FILTER_PY_FILES = Gtk.FileFilter()
FILTER_PY_FILES.set_name(name='Python')
FILTER_PY_FILES.add_pattern(pattern='*.py')
FILTER_PY_FILES.add_mime_type(mime_type='text/x-python')

FILTER_TXT_FILES = Gtk.FileFilter()
FILTER_TXT_FILES.set_name(name='txt')
FILTER_TXT_FILES.add_pattern(pattern='*.txt')
FILTER_TXT_FILES.add_mime_type(mime_type='text/plain')


class ExampleWindow(Gtk.ApplicationWindow):
    gio_list_store = Gio.ListStore.new(Gtk.FileFilter)
    gio_list_store.append(item=FILTER_ALL_FILES)
    gio_list_store.append(item=FILTER_PY_FILES)
    gio_list_store.append(item=FILTER_TXT_FILES)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        button_save = Gtk.Button.new_with_label(label='Save')
        button_save.connect('clicked', self.on_button_save_clicked)
        vbox.append(child=button_save)

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
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
