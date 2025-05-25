# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gettext
import locale
import pathlib

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk

APPLICATION_ID = 'br.com.justcode.Gtk'

BASE_DIR = pathlib.Path(__file__).resolve().parent
LOC_DIR = BASE_DIR / 'locale'

language_code = locale.getlocale()[0] or 'en_US'
lang = gettext.translation(
    domain=APPLICATION_ID,
    localedir=LOC_DIR,
    languages=[language_code],
    fallback=True,
)
lang.install()
_ = lang.gettext


class ExampleWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label=_('Preferences'),
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
        label.set_text(_('Hello World!'))
        label.set_vexpand(True)
        vbox.append(child=label)


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id=APPLICATION_ID,
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
