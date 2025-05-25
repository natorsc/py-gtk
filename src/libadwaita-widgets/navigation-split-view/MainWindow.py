# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, GLib, Gtk

Adw.init()


class Sidebar(Adw.NavigationPage):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_title(title='Sidebar')
        self.set_tag(tag='sidebar')

        self.adw_navigation_split_view = kwargs.get(
            'adw_navigation_split_view',
        )

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_child(child=adw_toolbar_view)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        # Top bar.
        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        # Menu buttons.
        menu_button_search = Gtk.Button.new()
        menu_button_search.set_icon_name(icon_name='system-search')
        adw_header_bar.pack_start(child=menu_button_search)

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        # Content.
        scrolled_window = Gtk.ScrolledWindow()
        adw_toolbar_view.set_content(content=scrolled_window)

        list_box = Gtk.ListBox.new()
        list_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        list_box.add_css_class(css_class='navigation-sidebar')
        list_box.connect('row-activated', self.on_row_clicked_change_page)
        scrolled_window.set_child(child=list_box)

        for item in ['Page 01', 'Page 02']:
            row = Gtk.ListBoxRow.new()
            row.set_child(Gtk.Label.new(str=item))
            list_box.append(child=row)

    def on_row_clicked_change_page(self, list_box, list_box_row):
        match list_box_row.get_child().get_label():
            case 'Page 01':
                self.adw_navigation_split_view.set_content(content=Page01())
            case 'Page 02':
                self.adw_navigation_split_view.set_content(content=Page02())
            case _:
                pass
        self.adw_navigation_split_view.set_show_content(show_content=True)


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
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        label = Gtk.Label.new(str='Page 01')
        vbox.append(child=label)


class Page02(Adw.NavigationPage):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_title(title='Title page 02')
        self.set_tag(tag='page-02')

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        label = Gtk.Label.new(str='Page 02')
        vbox.append(child=label)


class ExampleWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=600, height=300)

        adw_navigation_split_view = Adw.NavigationSplitView.new()
        adw_navigation_split_view.set_sidebar(
            sidebar=Sidebar(
                adw_navigation_split_view=adw_navigation_split_view
            )
        )
        adw_navigation_split_view.set_content(content=Page01())
        self.set_content(content=adw_navigation_split_view)

        breakpoint_condition = Adw.BreakpointCondition.new_length(
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=680,
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
