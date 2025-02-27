# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import configparser
import gettext
import pathlib

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk



APPLICATION_ID = 'br.com.justcode.PyGObject'


LOCALES_DIR = BASE_DIR.joinpath('locales')
CONFIG_FILE = BASE_DIR.joinpath('config.ini')
window_title = 'Python and GTK: Gtk.ApplicationWindow()'

# The default language of the operating system will be used.
# gettext.bindtextdomain(APPLICATION_ID, LOCALES_DIR)
# gettext.textdomain(APPLICATION_ID)
_ = gettext.gettext

config = configparser.ConfigParser()
if CONFIG_FILE.exists():
    config.read(CONFIG_FILE)
    language = config[APPLICATION_ID]['language']
    if language != 'default':
        lang = gettext.translation(
            APPLICATION_ID, localedir=LOCALES_DIR, languages=[language]
        )
        lang.install()
        _ = lang.gettext


class ExampleWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            _('Python and GTK: PyGObject internacionalização com gettext().'),
        )
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

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

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_bottom(12)
        vbox.set_margin_end(12)
        vbox.set_margin_start(12)
        vbox.set_margin_top(12)
        self.set_child(child=vbox)

        label = Gtk.Label.new()
        label.set_text(_('Após trocar o idioma reinicie o aplicativo.'))
        label.set_vexpand(True)
        vbox.append(child=label)

        combobox_text = Gtk.ComboBoxText()
        combobox_text.append_text(_('Selecione um idioma.'))
        combobox_text.set_active(0)
        combobox_text.connect('changed', self.combobox_text_changed)
        vbox.append(child=combobox_text)

        langs = ['en_US', 'pt_BR']
        for lang in langs:
            combobox_text.append_text(lang)

    def combobox_text_changed(self, combobox):
        row = combobox.get_active()
        if row != 0:
            text = combobox.get_active_text()
            print(f'O idioma selecionado foi: {text}')
            if text == 'pt_BR':
                text = 'default'

            config[APPLICATION_ID] = {'language': text}
            with open(CONFIG_FILE, 'w+') as f:
                config.write(f)
                f.close()


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
            flags=Gio.ApplicationFlags.FLAGS_NONE,
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
