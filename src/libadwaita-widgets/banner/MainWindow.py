# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject libadwaita Adw.Banner()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK: PyGObject libadwaita Adw.Banner()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(content=vbox)

        header_bar = Gtk.HeaderBar.new()
        vbox.append(child=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        overlay = Gtk.Overlay.new()
        vbox.append(child=overlay)

        self.banner = Adw.Banner.new(title='Banner title.')
        self.banner.set_button_label('Close')
        self.banner.set_valign(align=Gtk.Align.START)
        self.banner.connect('button-clicked', self.on_button_banner_clicked)
        overlay.add_overlay(widget=self.banner)

        button = Gtk.Button.new_with_label(label='Click here')
        button.set_vexpand(expand=True)
        button.set_valign(align=Gtk.Align.CENTER)
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        self.banner.set_revealed(revealed=True)

    def on_button_banner_clicked(self, banner):
        self.banner.set_revealed(revealed=False)


class ExampleApplication(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.PyGObject',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

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