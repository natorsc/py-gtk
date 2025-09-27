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

        # Top Bar.
        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        # Content.
        vbox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        vbox.set_margin_top(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        vbox.set_margin_end(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        button_open_shortcuts = Gtk.Button.new_with_label(label='Click here')
        # button_open_shortcuts.set_valign(align=Gtk.Align.CENTER)
        button_open_shortcuts.connect(
            'clicked', self.on_open_button_open_shortcuts_clicked
        )
        vbox.append(child=button_open_shortcuts)

    def on_open_button_open_shortcuts_clicked(self, widget):
        adw_shortcuts_section = Adw.ShortcutsSection.new(title='Section 01')

        adw_shortcuts_item = Adw.ShortcutsItem.new(
            title='Item 01', accelerator='<Shift>A'
        )
        adw_shortcuts_section.add(item=adw_shortcuts_item)

        adw_shortcuts_quit = Adw.ShortcutsItem.new_from_action(
            title='Quit',
            action_name='app.quit',
        )
        adw_shortcuts_quit.set_accelerator(accelerator='<Control>q')
        adw_shortcuts_section.add(item=adw_shortcuts_quit)

        adw_shortcuts_dialog = Adw.ShortcutsDialog.new()
        adw_shortcuts_dialog.set_size_request(width=683, height=384)
        adw_shortcuts_dialog.add(section=adw_shortcuts_section)
        adw_shortcuts_dialog.present()


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
