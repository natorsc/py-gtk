# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()

ITEMS = ['Item 01', 'Item 02', 'Item 03', 'Item 04', 'Item 05']


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

        self.listbox = Gtk.ListBox.new()
        self.listbox.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.listbox.add_css_class(css_class='boxed-list')
        vbox.append(child=self.listbox)

        model = Gtk.StringList.new(strings=ITEMS)

        for n in range(1, 5):
            icon = Gtk.Image.new_from_icon_name(
                icon_name='accessories-text-editor-symbolic'
            )

            adw_combo_row = Adw.ComboRow.new()
            adw_combo_row.set_title(title=f'Title {n}')
            adw_combo_row.set_subtitle(subtitle='Adw.ComboRow')
            adw_combo_row.add_prefix(widget=icon)
            adw_combo_row.set_model(model=model)
            adw_combo_row.connect(
                'notify::selected',
                self.on_adw_combo_row_selected,
            )
            adw_combo_row.connect(
                'notify::selected-item',
                self.on_adw_combo_row_selected_item,
            )
            self.listbox.append(child=adw_combo_row)

    def on_adw_combo_row_selected(self, comborow, GParamUInt):
        print(f'Position of the selected item {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Text of the selected item {selected_item.get_string()}')

    def on_adw_combo_row_selected_item(self, comborow, GParamObject):
        print(f'Position of the selected item {comborow.get_selected()}')
        selected_item = comborow.get_selected_item()
        print(f'Text of the selected item {selected_item.get_string()}')


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
