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
        self.set_size_request(width=600, height=300)

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_content(adw_toolbar_view)

        adw_view_stack = Adw.ViewStack.new()
        adw_toolbar_view.set_content(content=adw_view_stack)

        adw_view_switcher = Adw.ViewSwitcher.new()
        adw_view_switcher.set_stack(stack=adw_view_stack)
        adw_view_switcher.set_policy(policy=Adw.ViewSwitcherPolicy.WIDE)

        adw_view_switcher_bar_bottom = Adw.ViewSwitcherBar.new()
        adw_view_switcher_bar_bottom.set_stack(stack=adw_view_stack)
        adw_toolbar_view.add_bottom_bar(widget=adw_view_switcher_bar_bottom)

        adw_header_bar = Adw.HeaderBar.new()
        adw_header_bar.set_title_widget(title_widget=adw_view_switcher)
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        # Page 01.
        adw_status_page_01 = Adw.StatusPage.new()
        adw_status_page_01.set_title(title='Page 01')
        adw_view_stack.add_titled_with_icon(
            child=adw_status_page_01,
            name='page-01',
            title='Page 01',
            icon_name='user-desktop-symbolic',
        )

        # Page 02.
        adw_status_page_02 = Adw.StatusPage.new()
        adw_status_page_02.set_title(title='Page 02')

        adw_view_stack.add_titled_with_icon(
            child=adw_status_page_02,
            name='page-02',
            title='Page 02',
            icon_name='user-home-symbolic',
        )

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=680,
            unit=Adw.LengthUnit.PX,
        )
        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        break_point.add_setters(
            objects=[adw_view_switcher_bar_bottom, adw_header_bar],
            names=['reveal', 'title-widget'],
            values=[True, Gtk.Label.new(str=self.get_title())],
        )
        self.add_breakpoint(breakpoint=break_point)


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
