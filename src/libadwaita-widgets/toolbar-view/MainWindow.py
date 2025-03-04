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

        adw_toast_overlay = Adw.ToastOverlay.new()
        self.set_content(content=adw_toast_overlay)

        adw_toolbar_view = Adw.ToolbarView.new()
        adw_toast_overlay.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        adw_preferences_page = Adw.PreferencesPage.new()
        adw_toolbar_view.set_content(content=adw_preferences_page)

        button_flat = Gtk.Button.new_with_label(label='Suffix')
        button_flat.set_icon_name(icon_name='list-add-symbolic')
        button_flat.add_css_class(css_class='flat')

        adw_preferences_group = Adw.PreferencesGroup.new()
        adw_preferences_group.set_title(title='AdwPreferencesPage')
        adw_preferences_group.set_description(
            description='AdwPreferencesGroup'
        )
        adw_preferences_group.set_header_suffix(suffix=button_flat)
        adw_preferences_page.add(group=adw_preferences_group)

        switch_01 = Gtk.Switch.new()
        switch_01.set_valign(align=Gtk.Align.CENTER)

        adw_action_row_01 = Adw.ActionRow.new()
        adw_action_row_01.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='edit-find-symbolic'
            ),
        )
        adw_action_row_01.set_title(title='Libadwaita')
        adw_action_row_01.set_subtitle(subtitle='Adw.ActionRow')
        adw_action_row_01.add_suffix(widget=switch_01)
        adw_preferences_group.add(child=adw_action_row_01)

        switch_02 = Gtk.Switch.new()
        switch_02.set_valign(align=Gtk.Align.CENTER)

        adw_action_row_02 = Adw.ActionRow.new()
        adw_action_row_02.add_prefix(
            widget=Gtk.Image.new_from_icon_name(
                icon_name='edit-find-symbolic'
            ),
        )
        adw_action_row_02.set_title(title='Libadwaita')
        adw_action_row_02.set_subtitle(subtitle='Adw.ActionRow')
        adw_action_row_02.add_suffix(widget=switch_02)
        adw_action_row_02.set_activatable_widget(widget=switch_02)
        adw_preferences_group.add(child=adw_action_row_02)

        # Barra inferior.
        hbox_bottom_bar = Gtk.Box.new(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=12
        )
        hbox_bottom_bar.set_margin_top(margin=12)
        hbox_bottom_bar.set_margin_end(margin=12)
        hbox_bottom_bar.set_margin_bottom(margin=12)
        hbox_bottom_bar.set_margin_start(margin=12)
        adw_toolbar_view.add_bottom_bar(widget=hbox_bottom_bar)

        label = Gtk.Label.new()
        label.set_text(str='Adw.ToolbarView - Barra inferior')
        hbox_bottom_bar.append(child=label)


class ExampleApplication(Adw.Application):
    def __init__(self):
        super().__init__(
            application_id='nators.com.github.PyGtk',
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
