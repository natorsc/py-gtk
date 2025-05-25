# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

ITEMS = ['Title 01', 'Title 02', 'Title 03', 'Title 04', 'Title 05']


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_content(adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        self.list_box = Gtk.ListBox.new()
        self.list_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.list_box.add_css_class(css_class='boxed-list')
        vbox.append(child=self.list_box)

        for item in ITEMS:
            icon = Gtk.Image.new_from_icon_name(
                icon_name='accessories-text-editor-symbolic',
            )

            adw_entry_row = Adw.EntryRow.new()
            adw_entry_row.set_title(title=item)
            adw_entry_row.add_prefix(widget=icon)
            adw_entry_row.set_show_apply_button(show_apply_button=True)
            adw_entry_row.set_activates_default(activates=True)
            adw_entry_row.connect('apply', self.on_apply_button_pressed)
            self.list_box.append(child=adw_entry_row)

    def on_apply_button_pressed(self, entry_row):
        print(f'Entry value = {entry_row.get_text()}')


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

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
