# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent.parent.parent / 'scripts'))

from blp import blp_to_ui

UI_FILE = BASE_DIR / 'MainWindow.ui'
BLP_FILE = BASE_DIR / 'MainWindow.blp'
blp_to_ui(file=BLP_FILE)


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


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    adw_navigation_split_view = Gtk.Template.Child(
        name='adw_navigation_split_view'
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.adw_navigation_split_view.set_content(content=Page01())

    @Gtk.Template.Callback()
    def on_sidebar_activated_cb(self, sidebar, index):
        match sidebar.get_item(index).get_title():
            case 'Item 01':
                self.adw_navigation_split_view.set_content(content=Page01())
            case 'Item 02':
                self.adw_navigation_split_view.set_content(content=Page02())
            case _:
                pass
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
    app = ExampleApplication()
    app.run(sys.argv)
