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

BLP_FILE = BASE_DIR / 'MainWindow.blp'
SIDEBAR_BLP_FILE = BASE_DIR / 'Sidebar.blp'
PAGE01_BLP_FILE = BASE_DIR / 'Page01.blp'
PAGE02_BLP_FILE = BASE_DIR / 'Page02.blp'

UI_FILE = BASE_DIR / 'MainWindow.ui'
SIDEBAR_UI_FILE = BASE_DIR / 'Sidebar.ui'
PAGE01_UI_FILE = BASE_DIR / 'Page01.ui'
PAGE02_UI_FILE = BASE_DIR / 'Page02.ui'


blp_to_ui(file=BLP_FILE)
blp_to_ui(file=SIDEBAR_BLP_FILE)
blp_to_ui(file=PAGE01_BLP_FILE)
blp_to_ui(file=PAGE02_BLP_FILE)

Adw.init()

print(SIDEBAR_UI_FILE)
print(SIDEBAR_BLP_FILE)


@Gtk.Template(filename=SIDEBAR_UI_FILE)
class Sidebar(Adw.NavigationPage):
    __gtype_name__ = 'Sidebar'

    list_box = Gtk.Template.Child('list_box')

    def __init__(self, **kwargs):
        super().__init__()
        self.adw_navigation_split_view = kwargs.get(
            'adw_navigation_split_view'
        )

        PAGES = ['Page 01', 'Page 02']
        for page in PAGES:
            row = Gtk.ListBoxRow.new()
            row.set_child(Gtk.Label.new(str=page))
            self.list_box.append(child=row)

    @Gtk.Template.Callback()
    def on_row_clicked_change_page(self, list_box, list_box_row):
        match list_box_row.get_child().get_label():
            case 'Page 01':
                self.adw_navigation_split_view.set_content(Page01())
            case 'Page 02':
                self.adw_navigation_split_view.set_content(Page02())
            case _:
                pass
        self.adw_navigation_split_view.set_show_content(True)


@Gtk.Template(filename=PAGE01_UI_FILE)
class Page01(Adw.NavigationPage):
    __gtype_name__ = 'Page01'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(filename=PAGE02_UI_FILE)
class Page02(Adw.NavigationPage):
    __gtype_name__ = 'Page02'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Adw.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    adw_navigation_split_view = Gtk.Template.Child('adw_navigation_split_view')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.adw_navigation_split_view.set_sidebar(
            sidebar=Sidebar(
                adw_navigation_split_view=self.adw_navigation_split_view
            )
        )
        self.adw_navigation_split_view.set_content(content=Page01())
        # self.set_content(content=adw_navigation_split_view)


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
    app = ExampleApplication()
    app.run(sys.argv)
