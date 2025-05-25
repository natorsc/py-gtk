# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_content(content=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        self.adw_toast_overlay = Adw.ToastOverlay.new()
        adw_toolbar_view.set_content(content=self.adw_toast_overlay)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.adw_toast_overlay.set_child(child=vbox)

        button = Gtk.Button.new_with_label(label='Click here')
        button.set_valign(align=Gtk.Align.CENTER)
        button.set_vexpand(expand=True)
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        toast = Adw.Toast.new(title='Lorem Ipsum')
        toast.set_button_label(button_label='Undo')
        toast.set_action_name(action_name='app.toast')
        toast.connect('dismissed', self.on_toast_dismissed)
        toast.connect('button-clicked', self.on_toast_button_clicked)
        self.adw_toast_overlay.add_toast(toast)

    def on_toast_dismissed(self, toast):
        print('[!] on_toast_dismissed [!]')

    def on_toast_button_clicked(self, toast):
        print('[!] on_toast_button_clicked [!]')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])

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
