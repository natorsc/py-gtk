# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

        self.adw_toast_overlay = Adw.ToastOverlay.new()
        self.set_content(content=self.adw_toast_overlay)

        adw_toolbar_view = Adw.ToolbarView.new()
        self.adw_toast_overlay.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        self.button = Gtk.Button.new_with_label(label='Click here')
        self.button.set_vexpand(expand=True)
        self.button.set_valign(align=Gtk.Align.END)
        self.button.connect('clicked', self.on_button_clicked)
        vbox.append(child=self.button)

        self.toast = Adw.Toast.new(title='Lorem Ipsum')
        self.toast.set_button_label(button_label='Undo')
        self.toast.set_action_name(action_name='app.toast')
        self.toast.connect('dismissed', self.on_toast_dismissed)
        self.toast.connect('button-clicked', self.on_toast_button_clicked)

    def on_button_clicked(self, button):
        button.set_sensitive(sensitive=False)
        self.adw_toast_overlay.add_toast(self.toast)

    def on_toast_dismissed(self, toast):
        """Emitted when the toast has been dismissed."""
        print('[!] dismissed [!]')
        print('Emitted when the toast has been dismissed')
        self.button.set_sensitive(sensitive=True)

    def on_toast_button_clicked(self, toast):
        """Emitted after the button has been clicked."""
        print('[!] button-clicked [!]')
        print('Emitted after the button has been clicked.')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('toast', self.on_toast_action)

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

    def on_toast_action(self, action, param):
        """It will be activated when clicking the button."""
        print('[!] action-name [!]')
        print('Action `app.toast` was active.')
        print('It will be activated when clicking the button')

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
