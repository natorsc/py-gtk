# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):
    items = ['Item 01', 'Item 02', 'Item 03', 'Item 04', 'Item 05']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')

        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

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

        self.listbox = Gtk.ListBox.new()
        self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.listbox.add_css_class(css_class='boxed-list')
        self.listbox.set_margin_start(margin=12)
        self.listbox.set_margin_end(margin=12)
        vbox.append(child=self.listbox)

        for item in self.items:
            icon = Gtk.Image.new_from_icon_name(
                icon_name='accessories-text-editor-symbolic',
            )

            switch = Gtk.Switch.new()
            switch.set_valign(align=Gtk.Align.CENTER)
            switch.connect('notify::active', self.on_switch_button_clicked)

            adw_action_row = Adw.ActionRow.new()
            adw_action_row.set_title(title=item)
            adw_action_row.set_subtitle(subtitle='Adw.ActionRow')
            adw_action_row.add_prefix(widget=icon)
            adw_action_row.add_suffix(widget=switch)
            self.listbox.append(child=adw_action_row)

    def on_switch_button_clicked(self, switch, GParamBoolean):
        if switch.get_active():
            print('Button checked')
        else:
            print('Button unchecked')


class ExampleApplication(Adw.Application):
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
