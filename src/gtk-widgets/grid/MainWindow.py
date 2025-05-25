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

        grid = Gtk.Grid.new()
        grid.set_margin_top(margin=12)
        grid.set_margin_end(margin=12)
        grid.set_margin_bottom(margin=12)
        grid.set_margin_start(margin=12)
        grid.set_row_spacing(spacing=12)
        grid.set_column_spacing(spacing=12)
        self.set_child(child=grid)

        button1 = Gtk.Button.new_with_label(label='Button 1')
        button2 = Gtk.Button.new_with_label(label='Button 2')
        button3 = Gtk.Button.new_with_label(label='Button 3')
        button4 = Gtk.Button.new_with_label(label='Button 4')
        button5 = Gtk.Button.new_with_label(label='Button 5')
        button6 = Gtk.Button.new_with_label(label='Button 6')

        # Adding sequentially.
        # grid.add(widget=button1)
        # grid.add(widget=button2)
        # grid.add(widget=button3)
        # grid.add(widget=button4)
        # grid.add(widget=button5)
        # grid.add(widget=button6)

        # Positioning using attach()
        # Determining the position based on columns and rows.
        # grid.attach(child=button1, left=0, top=0, width=1, height=1)
        # grid.attach(child=button2, left=1, top=0, width=1, height=1)
        # grid.attach(child=button3, left=0, top=1, width=1, height=1)
        # grid.attach(child=button4, left=1, top=1, width=1, height=1)
        # grid.attach(child=button5, left=0, top=2, width=1, height=1)
        # grid.attach(child=button6, left=1, top=2, width=1, height=1)

        # Positioning using attach_next_to()
        # In this positioning we use other widgets as references.
        # Button 1 is in column 0 and row 0
        grid.attach(child=button1, column=0, row=0, width=1, height=1)
        # Button 2 is in column 1 and row 0 and merges 2 columns and 1 row.
        grid.attach(child=button2, column=1, row=0, width=2, height=1)
        # Button 3 is referenced to Button 1, it should be below
        # Button 1 (BOTTOM), it merges 1 column and 2 rows.
        grid.attach_next_to(
            child=button3,
            sibling=button1,
            side=Gtk.PositionType.BOTTOM,
            width=1,
            height=2,
        )
        # Button 4 is referenced to Button 3, it should be to the right of
        # Button 3 (RIGHT), it merges 2 columns and 1 row.
        grid.attach_next_to(
            child=button4,
            sibling=button3,
            side=Gtk.PositionType.RIGHT,
            width=2,
            height=1,
        )
        # Button 5 is in column 1, row 2 and merges 1 column and 1 row.
        grid.attach(child=button5, column=1, row=2, width=1, height=1)
        # Button 6 is referenced to Button 5, it should be to the right of
        # Button 5 (RIGHT), it merges 1 column and 1 row.
        grid.attach_next_to(
            child=button6,
            sibling=button5,
            side=Gtk.PositionType.RIGHT,
            width=1,
            height=1,
        )


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
