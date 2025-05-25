# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk


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
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        button_mail = Gtk.Button.new_from_icon_name(
            icon_name='mail-send-receive-symbolic',
        )
        button_mail.connect('clicked', self.on_button_send_mail_cliqued)
        header_bar.pack_end(child=button_mail)

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        header_bar.pack_start(child=hbox)

        button_left_arrow = Gtk.Button.new_from_icon_name(
            icon_name='go-previous-symbolic',
        )
        button_left_arrow.connect('clicked', self.on_button_left_arrow_cliqued)
        hbox.append(child=button_left_arrow)

        button_right_arrow = Gtk.Button.new_from_icon_name(
            icon_name='go-previous-symbolic-rtl',
        )
        button_right_arrow.connect(
            'clicked', self.on_button_right_arrow_cliqued
        )
        hbox.append(child=button_right_arrow)

    @staticmethod
    def on_button_send_mail_cliqued(button):
        print('You clicked on the button with the send/receive email icon')

    @staticmethod
    def on_button_left_arrow_cliqued(butthon):
        print('You clicked on the button with the left arrow')

    @staticmethod
    def on_button_right_arrow_cliqued(button):
        print('You clicked on the button with the right arrow')


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
