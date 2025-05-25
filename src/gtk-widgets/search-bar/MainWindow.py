# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk


class ExampleWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=683, height=384)
        self.set_size_request(width=683, height=384)

        header_bar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        header_bar.pack_end(child=menu_button)

        button_show_searchbar = Gtk.ToggleButton.new()
        button_show_searchbar.set_icon_name(icon_name='system-search-symbolic')
        button_show_searchbar.connect(
            'clicked',
            self.on_button_show_searchbar_clicked,
        )
        header_bar.pack_start(child=button_show_searchbar)

        overlay = Gtk.Overlay.new()
        self.set_child(child=overlay)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        overlay.set_child(child=vbox)

        entry = Gtk.Entry.new()
        entry.set_placeholder_text(text='GtkSearchBar')
        entry.set_icon_from_icon_name(
            icon_pos=Gtk.EntryIconPosition.PRIMARY,
            icon_name='system-search-symbolic',
        )
        entry.connect('activate', self.on_key_enter_pressed)
        entry.connect('icon-press', self.on_icon_pressed)

        self.search_bar = Gtk.SearchBar.new()
        # self.search_bar.set_show_close_button(visible=True)
        self.search_bar.set_child(child=entry)
        self.search_bar.add_css_class(css_class='inline')
        self.search_bar.set_halign(align=Gtk.Align.START)
        self.search_bar.set_valign(align=Gtk.Align.START)
        overlay.add_overlay(widget=self.search_bar)

        label = Gtk.Label.new(str='Click on the search icon.')
        label.set_vexpand(expand=True)
        vbox.append(child=label)

    def on_button_show_searchbar_clicked(self, toggle_button):
        if self.search_bar.get_search_mode():
            self.search_bar.set_search_mode(search_mode=False)
        else:
            self.search_bar.set_search_mode(search_mode=True)

    def on_icon_pressed(self, entry, entry_icon_position):
        print('Ícone pressionado.')

    def on_key_enter_pressed(self, entry):
        print('Enter pressionando.')


class ExampleApplication(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id='br.com.justcode.Gtk',
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
