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

        adw_status_page = Adw.StatusPage.new()
        adw_status_page.set_title(title='Adw.Breakpoint')
        adw_status_page.set_icon_name('audio-volume-high-symbolic')
        adw_toolbar_view.set_content(content=adw_status_page)

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            # MAX_HEIGHT, MAX_WIDTH, MIN_HEIGHT, MIN_WIDTH.
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=700,
            # PT, PX, SP.
            unit=Adw.LengthUnit.PX,
        )
        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        break_point.add_setter(
            object=adw_status_page,
            property='icon-name',
            value='audio-volume-muted-symbolic',
        )
        # break_point.add_setters(
        #     objects=[adw_status_page],
        #     names=['icon-name'],
        #     values=['audio-volume-muted-symbolic'],
        # )
        self.add_breakpoint(breakpoint=break_point)


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
        )

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action(
            name='preferences',
            callback=self.on_preferences_action,
            shortcuts=['<Primary>comma'],
        )

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
