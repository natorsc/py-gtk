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
        self.set_title(title='Page 01')
        self.set_tag(tag='page-01')

        self.adw_navigation_view = kwargs.get('adw_navigation_view')

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_child(child=adw_toolbar_view)

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
        label.set_vexpand(expand=True)
        vbox.append(child=label)

        button = Gtk.Button.new_with_label(label='Go to page 02')
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, widget):
        self.adw_navigation_view.push_by_tag(tag='page-02')


class Page02(Adw.NavigationPage):
    def __init__(self, **kwargs):
        super().__init__()
        self.set_title(title='Page 02')
        self.set_tag(tag='page-02')

        self.adw_navigation_view = kwargs.get('adw_navigation_view')

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
        self.set_size_request(width=683, height=384)

        adw_navigation_view = Adw.NavigationView.new()
        adw_navigation_view.add(
            page=Page01(adw_navigation_view=adw_navigation_view),
        )
        adw_navigation_view.add(
            page=Page02(adw_navigation_view=adw_navigation_view),
        )
        self.set_content(content=adw_navigation_view)


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
