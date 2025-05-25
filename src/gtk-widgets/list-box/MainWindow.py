# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk


class ExampleWindow(Gtk.ApplicationWindow):
    itens = ['Item 01', 'Item 02', 'Item 03']

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
        vbox.set_homogeneous(homogeneous=True)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        list_box_01 = Gtk.ListBox.new()
        list_box_01.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        vbox.append(child=list_box_01)

        for n in range(1, 4):
            list_box_row = Gtk.ListBoxRow.new()
            list_box_row.set_selectable(selectable=False)

            hbox = Gtk.Box.new(
                orientation=Gtk.Orientation.HORIZONTAL, spacing=0
            )

            list_box_row.set_child(child=hbox)

            label = Gtk.Label.new(str=f'Line 0{n}')
            label.set_margin_top(margin=6)
            label.set_margin_end(margin=6)
            label.set_margin_bottom(margin=6)
            label.set_margin_start(margin=6)
            label.set_xalign(xalign=0)
            label.set_hexpand(expand=True)
            hbox.append(child=label)

            switch = Gtk.Switch.new()
            switch.set_margin_top(margin=6)
            switch.set_margin_end(margin=6)
            switch.set_margin_bottom(margin=6)
            switch.set_margin_start(margin=6)
            hbox.append(child=switch)

            list_box_01.append(child=list_box_row)

        list_box_02 = Gtk.ListBox.new()
        list_box_02.connect('row-activated', self.on_row_clicked)
        vbox.append(child=list_box_02)

        for item in self.itens:
            label = Gtk.Label.new(str=item)
            label.set_margin_top(6)
            label.set_margin_bottom(6)
            list_box_02.append(child=label)

    def on_row_clicked(self, listbox, listboxrow):
        print(f'Clicou no {self.itens[listboxrow.get_index()]}')


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
