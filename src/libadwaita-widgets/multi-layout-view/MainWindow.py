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
        # self.set_size_request(width=683, height=384)

        # Adw.MultiLayoutView.
        adw_multi_layout_view = Adw.MultiLayoutView.new()
        self.set_content(content=adw_multi_layout_view)

        # Desktop layout.
        adw_overlay_split_view = Adw.OverlaySplitView.new()
        adw_overlay_split_view.set_sidebar(
            sidebar=Adw.LayoutSlot.new(id='slot-sidebar')
        )
        adw_overlay_split_view.set_content(
            content=Adw.LayoutSlot.new(id='slot-content')
        )

        adw_layout_desktop = Adw.Layout.new(content=adw_overlay_split_view)
        adw_layout_desktop.set_name('desktop')
        adw_multi_layout_view.add_layout(adw_layout_desktop)

        # Mobile layout.
        vbox_bottom_bar = Gtk.Box.new(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0,
        )
        vbox_bottom_bar.set_margin_top(margin=20)
        vbox_bottom_bar.set_margin_end(margin=12)
        vbox_bottom_bar.set_margin_bottom(margin=12)
        vbox_bottom_bar.set_margin_start(margin=12)

        label = Gtk.Label.new(str='Adw.BottomSheet bottom-bar')
        vbox_bottom_bar.append(child=label)

        adw_bottom_sheet = Adw.BottomSheet.new()
        adw_bottom_sheet.set_bottom_bar(bottom_bar=vbox_bottom_bar)
        adw_bottom_sheet.set_sheet(sheet=Adw.LayoutSlot.new(id='slot-sidebar'))
        adw_bottom_sheet.set_content(
            content=Adw.LayoutSlot.new(id='slot-content')
        )

        adw_layout_mobile = Adw.Layout.new(content=adw_bottom_sheet)
        adw_layout_mobile.set_name('mobile')
        adw_multi_layout_view.add_layout(adw_layout_mobile)

        # Main content [slot-content].
        adw_toolbar_view = Adw.ToolbarView.new()
        adw_toolbar_view.add_top_bar(widget=Adw.HeaderBar.new())

        adw_status_page = Adw.StatusPage.new()
        adw_status_page.set_title(title='Adw.MultiLayoutView')
        adw_status_page.set_description(
            description='Adw.Layout - Adw.LayoutSlot'
        )
        adw_toolbar_view.set_content(content=adw_status_page)
        # Adding slot in Adw.MultiLayoutView.
        adw_multi_layout_view.set_child(
            id='slot-content', child=adw_toolbar_view
        )

        # Sidebar content [slot-sidebar].
        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        vbox.set_margin_top(margin=20)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)

        list_box = Gtk.ListBox.new()
        list_box.add_css_class(css_class='navigation-sidebar')
        vbox.append(child=list_box)

        for i in range(1, 4):
            row = Gtk.ListBoxRow.new()
            row.set_child(Gtk.Label.new(str=f'Item {i}'))
            list_box.append(child=row)
        # Adding slot in Adw.MultiLayoutView.
        adw_multi_layout_view.set_child(id='slot-sidebar', child=vbox)

        # Breakpoint.
        breakpoint_condition = Adw.BreakpointCondition.new_length(
            # MAX_HEIGHT, MAX_WIDTH, MIN_HEIGHT, MIN_WIDTH.
            type=Adw.BreakpointConditionLengthType.MAX_WIDTH,
            value=600,
            # PT, PX, SP.
            unit=Adw.LengthUnit.PX,
        )
        break_point = Adw.Breakpoint.new(condition=breakpoint_condition)
        break_point.add_setter(
            object=adw_multi_layout_view,
            property='layout-name',
            value='mobile',
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
