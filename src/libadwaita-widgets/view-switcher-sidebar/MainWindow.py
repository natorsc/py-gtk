# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class Page01(Adw.NavigationPage):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_title(title='Title page 01')
        self.set_tag(tag='page-01')

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_child(child=adw_toolbar_view)

        # Top bar.
        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        # Content.
        adw_status_page = Adw.StatusPage.new()
        adw_status_page.set_title(title='Page 01')
        adw_toolbar_view.set_content(content=adw_status_page)
        adw_toolbar_view.set_content(content=adw_status_page)


class Page02(Adw.NavigationPage):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_title(title='Title page 02')
        self.set_tag(tag='page-02')

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        adw_status_page = Adw.StatusPage.new()
        adw_status_page.set_title(title='Page 02')
        adw_toolbar_view.set_content(content=adw_status_page)


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)

        self.adw_navigation_split_view = Adw.NavigationSplitView.new()
        self.set_content(content=self.adw_navigation_split_view)

        # Page sidebar (Adw.NavigationSplitView).
        adw_toolbar_view_sidebar = Adw.ToolbarView.new()

        adw_header_bar_sidebar = Adw.HeaderBar.new()
        adw_toolbar_view_sidebar.add_top_bar(widget=adw_header_bar_sidebar)

        adw_view_switcher_sidebar = Adw.ViewSwitcherSidebar.new()
        adw_view_switcher_sidebar.connect(
            'activated', self.on_view_switcher_sidebar_activated_cb
        )
        adw_toolbar_view_sidebar.set_content(content=adw_view_switcher_sidebar)

        adw_navigation_page_sidebar = Adw.NavigationPage.new_with_tag(
            child=adw_toolbar_view_sidebar,
            title='Sidebar',
            tag='sidebar',
        )
        self.adw_navigation_split_view.set_sidebar(
            sidebar=adw_navigation_page_sidebar
        )

        # Page content (Adw.NavigationSplitView).
        adw_toolbar_view_content = Adw.ToolbarView.new()

        adw_view_stack = Adw.ViewStack.new()
        adw_view_switcher_sidebar.set_stack(stack=adw_view_stack)
        adw_toolbar_view_content.set_content(content=adw_view_stack)

        adw_navigation_page_content = Adw.NavigationPage.new_with_tag(
            child=adw_toolbar_view_content,
            title='Content',
            tag='content',
        )
        self.adw_navigation_split_view.set_content(
            content=adw_navigation_page_content
        )

        # Pages.
        adw_view_stack.add_titled_with_icon(
            child=Page01(),
            name='page-01',
            title='Page 01',
            icon_name='call-start-symbolic',
        )
        adw_view_stack.add_titled_with_icon(
            child=Page02(),
            name='page-02',
            title='Page 02',
            icon_name='call-start-symbolic',
        )

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            # MAX_HEIGHT, MAX_WIDTH, MIN_HEIGHT, MIN_WIDTH.
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=600,
            # PT, PX, SP.
            unit=Adw.LengthUnit.SP,
        )
        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        break_point.add_setter(
            object=self.adw_navigation_split_view,
            property='collapsed',
            value=True,
        )
        self.add_breakpoint(breakpoint=break_point)

    def on_view_switcher_sidebar_activated_cb(self, widget):
        self.adw_navigation_split_view.set_show_content(show_content=True)


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
