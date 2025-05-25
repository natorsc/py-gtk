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

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        check_button_group = Gtk.CheckButton.new()

        check_button_01 = Gtk.CheckButton.new_with_label(label='Item 01')
        check_button_01.set_name(name='check_button_01')
        check_button_01.set_active(setting=True)
        check_button_01.set_group(group=check_button_group)
        check_button_01.connect('toggled', self.on_radio_button_toggled)
        vbox.append(child=check_button_01)

        check_button_02 = Gtk.CheckButton.new_with_label(label='Item 02')
        check_button_02.set_name(name='check_button_02')
        check_button_02.set_group(group=check_button_group)
        check_button_02.connect('toggled', self.on_radio_button_toggled)
        vbox.append(child=check_button_02)

        check_button_03 = Gtk.CheckButton.new_with_label(label='Item 03')
        check_button_03.set_name(name='check_button_03')
        check_button_03.set_group(group=check_button_group)
        check_button_03.connect('toggled', self.on_radio_button_toggled)
        vbox.append(child=check_button_03)

    def on_radio_button_toggled(self, widget):
        if widget.get_active():
            print(f'Radio text: {widget.get_label()}')
            print(f'Widget name: {widget.get_name()}')


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
