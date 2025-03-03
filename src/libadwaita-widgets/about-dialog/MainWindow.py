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

        adw_toolbar_view = Adw.ToolbarView.new()

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        adw_navigation_page = Adw.NavigationPage.new(
            child=adw_toolbar_view,
            title='Title page 01',
        )
        self.set_content(adw_navigation_page)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        button = Gtk.Button.new_with_label(label='Click me')
        button.connect('clicked', self.on_button_clicked)
        vbox.append(child=button)

    def on_button_clicked(self, button):
        dialog = Adw.AboutDialog.new()
        dialog.set_application_name('Python - GTK - PyGObject.')
        dialog.set_version('0.0.1')
        dialog.set_developer_name('Renato Cruz (natorsc)')
        dialog.set_license_type(Gtk.License(Gtk.License.MIT_X11))
        dialog.set_comments(
            'Creating graphical interfaces with the Python programming '
            'language (PyGObject) and the GTK graphics toolkit'
        )
        dialog.set_website('https://github.com/natorsc/py-gtk/')
        dialog.set_issue_url('https://github.com/natorsc/py-gtk/issues')
        dialog.set_translator_credits('Renato Cruz')
        dialog.set_copyright('© 2022 Renato Cruz (natorsc)')
        dialog.set_developers(['natorsc https://github.com/natorsc'])
        dialog.set_application_icon('help-about-symbolic')
        dialog.present()


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='nators.com.github.PyGtk',
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
