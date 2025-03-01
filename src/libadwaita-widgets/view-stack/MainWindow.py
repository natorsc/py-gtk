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

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=550,
            unit=Adw.LengthUnit.PX,
        )

        title_widget = Gtk.Label.new()
        title_widget.set_text(str='teste')

        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        # break_point.add_setters(
        #     objects=[title_widget],
        #     # names=['switcher_bar.reveal', 'header_bar.title-widget'],
        #     names=['switcher_bar.reveal'],
        #     values=[True],
        # )

        self.add_breakpoint(breakpoint=break_point)
        print(self.get_current_breakpoint())

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_content(content=adw_toolbar_view)

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

        adw_view_stack = Adw.ViewStack.new()
        adw_toolbar_view.set_content(content=adw_view_stack)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)

        self.button = Gtk.Button.new_with_label(label='Click here')
        self.button.set_vexpand(expand=True)
        self.button.set_valign(align=Gtk.Align.END)
        vbox.append(child=self.button)

        page_01 = Adw.ViewStackPage(child=vbox)
        page_01.set_name(name='page01')
        page_01.set_title('ViewStackPage')


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
