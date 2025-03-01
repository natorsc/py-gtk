# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class Dialog(Adw.MessageDialog):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_heading(heading='Dialog header')
        self.set_body(body='Body of the dialog window, you can use markup.')
        self.add_response(Gtk.ResponseType.CANCEL.value_nick, 'Cancelar')
        self.set_response_appearance(
            response=Gtk.ResponseType.CANCEL.value_nick,
            appearance=Adw.ResponseAppearance.DESTRUCTIVE,
        )
        self.add_response(Gtk.ResponseType.OK.value_nick, 'OK')
        self.set_response_appearance(
            response=Gtk.ResponseType.OK.value_nick,
            appearance=Adw.ResponseAppearance.SUGGESTED,
        )
        self.connect('response', self.dialog_response)

    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK.value_nick:
            print('OK button pressed')
        elif response == Gtk.ResponseType.CANCEL.value_nick:
            print('CANCEL button pressed')


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')

        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

        adw_toast_overlay = Adw.ToastOverlay.new()
        self.set_content(content=adw_toast_overlay)

        adw_toolbar_view = Adw.ToolbarView.new()
        adw_toast_overlay.set_child(child=adw_toolbar_view)

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

        button = Gtk.Button.new_with_label(label='Click here')
        button.set_valign(align=Gtk.Align.CENTER)
        button.set_vexpand(expand=True)
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        # Using a class.
        # dialog = Dialog(transient_for=self)
        # dialog.present()

        dialog = Adw.MessageDialog.new(parent=self)
        dialog.set_heading(heading='Dialog header')
        dialog.set_body(
            body='Body of the dialog window, you can use markup.',
        )
        dialog.add_response(Gtk.ResponseType.CANCEL.value_nick, 'Cancelar')
        dialog.set_response_appearance(
            response=Gtk.ResponseType.CANCEL.value_nick,
            appearance=Adw.ResponseAppearance.DESTRUCTIVE,
        )
        dialog.add_response(Gtk.ResponseType.OK.value_nick, 'OK')
        dialog.set_response_appearance(
            response=Gtk.ResponseType.OK.value_nick,
            appearance=Adw.ResponseAppearance.SUGGESTED,
        )
        dialog.connect('response', self.dialog_response)
        dialog.present()

    def dialog_response(self, dialog, response):
        if response == Gtk.ResponseType.OK.value_nick:
            print('OK button pressed')
        elif response == Gtk.ResponseType.CANCEL.value_nick:
            print('CANCEL button pressed')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
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
