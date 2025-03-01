# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, GLib, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')

        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 3), height=int(768 / 3))

        # Sidebar.
        adw_toolbar_view_sidebar = Adw.ToolbarView.new()

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view_sidebar.add_top_bar(widget=adw_header_bar)

        menu_button_search = Gtk.Button.new()
        menu_button_search.set_icon_name(icon_name='system-search')
        adw_header_bar.pack_start(child=menu_button_search)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        navigation_page = Adw.NavigationPage.new(
            child=adw_toolbar_view_sidebar,
            title='sidebar',
        )

        adw_navigation_split_view = Adw.NavigationSplitView.new()
        adw_navigation_split_view.set_sidebar(sidebar=navigation_page)
        self.set_content(content=adw_navigation_split_view)

        list_box = Gtk.ListBox.new()
        list_box.add_css_class(css_class='navigation-sidebar')
        adw_toolbar_view_sidebar.set_content(content=list_box)

        row_item_01 = Gtk.ListBoxRow.new()
        row_item_01.set_child(Gtk.Label.new(str='Item 01'))
        row_item_01.set_action_name(action_name='navigation.push')
        row_item_01.set_action_target_value(
            target_value=GLib.Variant.new_string(string='item01')
        )
        list_box.append(child=row_item_01)

        # Item 01.
        adw_toolbar_view_item_01 = Adw.ToolbarView.new()

        adw_header_bar_item_01 = Adw.HeaderBar.new()
        adw_toolbar_view_item_01.add_top_bar(
            widget=adw_header_bar_item_01,
        )

        adw_navigation_page_item_01 = Adw.NavigationPage.new_with_tag(
            child=adw_toolbar_view_item_01,
            title='Title item 01',
            tag='item01',
        )
        adw_navigation_split_view.set_content(
            content=adw_navigation_page_item_01,
        )

        vbox_item_01 = Gtk.Box.new(
            orientation=Gtk.Orientation.VERTICAL, spacing=12
        )
        vbox_item_01.set_margin_top(margin=12)
        vbox_item_01.set_margin_end(margin=12)
        vbox_item_01.set_margin_bottom(margin=12)
        vbox_item_01.set_margin_start(margin=12)
        adw_toolbar_view_item_01.set_content(content=vbox_item_01)

        label_item_01 = Gtk.Label.new(str='Item 01')
        vbox_item_01.append(child=label_item_01)

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=500,
            unit=Adw.LengthUnit.PX,
        )
        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        break_point.add_setters(
            objects=[adw_navigation_split_view],
            names=['collapsed'],
            values=[True],
        )

        self.add_breakpoint(breakpoint=break_point)


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.PyGObject',
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
