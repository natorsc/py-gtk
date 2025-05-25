# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk


class ExampleWindow(Gtk.ApplicationWindow):
    itens = ['Item 01', 'Item 02', 'Item 03']

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

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        model_string_list = Gtk.StringList.new()
        model_string_list.append('Item 01')
        model_string_list.append('Item 02')
        model_string_list.append('Item 03')

        model_single_selection = Gtk.SingleSelection.new(
            model=model_string_list
        )
        # model_no_selection = Gtk.NoSelection.new(model=model_string_list)

        list_item_factory = Gtk.SignalListItemFactory.new()
        list_item_factory.connect('setup', self._setup_list_item)
        list_item_factory.connect('bind', self._bind_list_item)

        list_view = Gtk.ListView.new()
        list_view.set_model(model=model_single_selection)
        # list_view.set_model(model=model_no_selection)
        list_view.set_factory(factory=list_item_factory)
        list_view.connect('activate', self.on_list_view_row_activate)
        vbox.append(child=list_view)

    def _setup_list_item(self, factory, list_item):
        label = Gtk.Label()
        list_item.set_child(label)

    def _bind_list_item(self, factory, list_item):
        string_object = list_item.get_item()
        label = list_item.get_child()
        label.set_text(string_object.get_string())

    def on_list_view_row_activate(self, list_view, index):
        single_selection = list_view.get_model()
        string_object = single_selection.get_selected_item()
        print(index)
        print(single_selection.get_selected())
        print(string_object.get_string())


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
