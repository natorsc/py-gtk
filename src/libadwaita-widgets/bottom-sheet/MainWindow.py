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
        self.set_size_request(width=683, height=384)

        adw_toolbar_view = Adw.ToolbarView.new()
        self.set_content(content=adw_toolbar_view)

        # Top Bar.
        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        # Content (Adw.ToolbarView).
        self.adw_bottom_sheet = Adw.BottomSheet.new()
        adw_toolbar_view.set_content(content=self.adw_bottom_sheet)

        # Main window content (Adw.BottomSheet).
        adw_status_page = Adw.StatusPage.new()
        adw_status_page.set_title(title='Hello World!')
        self.adw_bottom_sheet.set_content(content=adw_status_page)

        # Content that is displayed in the bottom bar.
        bottom_bar_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )
        bottom_bar_box.set_margin_top(margin=12)
        bottom_bar_box.set_margin_bottom(margin=12)
        bottom_bar_box.set_margin_start(margin=12)
        bottom_bar_box.set_margin_end(margin=12)
        bottom_bar_box.add_css_class(css_class='toolbar')
        self.adw_bottom_sheet.set_bottom_bar(bottom_bar=bottom_bar_box)

        music_icon = Gtk.Image.new_from_icon_name('multimedia-player-symbolic')
        bottom_bar_box.append(child=music_icon)

        music_info_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=2,
        )
        music_info_box.set_hexpand(True)
        bottom_bar_box.append(child=music_info_box)

        title_label = Gtk.Label(label='Music')
        title_label.set_halign(Gtk.Align.START)
        title_label.add_css_class('heading')
        music_info_box.append(child=title_label)

        artist_label = Gtk.Label(label='Artist')
        artist_label.set_halign(Gtk.Align.START)
        artist_label.add_css_class('caption')
        music_info_box.append(child=artist_label)

        play_button = Gtk.Button.new_from_icon_name(
            icon_name='media-playback-start-symbolic',
        )
        play_button.add_css_class(css_class='circular')
        play_button.connect('clicked', self.on_play_button_clicked)
        bottom_bar_box.append(child=play_button)

        # Sliding (sheet) pane content.
        sheet_box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=12,
        )
        sheet_box.set_margin_top(margin=12)
        sheet_box.set_margin_bottom(margin=12)
        sheet_box.set_margin_start(margin=12)
        sheet_box.set_margin_end(margin=12)
        self.adw_bottom_sheet.set_sheet(sheet=sheet_box)

        header_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )
        sheet_box.append(child=header_box)

        album_image = Gtk.Image.new_from_icon_name(
            icon_name='multimedia-player-symbolic',
        )
        album_image.set_pixel_size(pixel_size=80)
        header_box.append(child=album_image)

        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        info_box.set_hexpand(True)
        header_box.append(child=info_box)

        title = Gtk.Label(label='Music')
        title.set_halign(align=Gtk.Align.START)
        title.add_css_class(css_class='title-2')
        info_box.append(child=title)

        artist = Gtk.Label(label='Artist')
        artist.set_halign(align=Gtk.Align.START)
        artist.add_css_class(css_class='title-4')
        info_box.append(child=artist)

        album = Gtk.Label(label='Album • 2025')
        album.set_halign(align=Gtk.Align.START)
        album.add_css_class(css_class='caption')
        info_box.append(child=album)
        progress_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )
        sheet_box.append(child=progress_box)

        current_time = Gtk.Label(label='2:00')
        current_time.add_css_class(css_class='caption')
        progress_box.append(child=current_time)

        progress_bar = Gtk.Scale.new_with_range(
            orientation=Gtk.Orientation.HORIZONTAL,
            min=0,
            max=100,
            step=1,
        )
        progress_bar.set_value(value=45)
        progress_bar.set_hexpand(expand=True)
        progress_bar.set_draw_value(draw_value=False)
        progress_box.append(child=progress_bar)

        total_time = Gtk.Label(label='3:00')
        total_time.add_css_class(css_class='caption')
        progress_box.append(child=total_time)

        controls_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=12,
        )
        controls_box.set_halign(align=Gtk.Align.CENTER)
        controls_box.set_margin_top(margin=12)
        sheet_box.append(child=controls_box)

        shuffle_btn = Gtk.Button.new_from_icon_name(
            icon_name='media-playlist-shuffle-symbolic',
        )
        shuffle_btn.add_css_class(css_class='circular')
        controls_box.append(child=shuffle_btn)

        prev_btn = Gtk.Button.new_from_icon_name(
            icon_name='media-skip-backward-symbolic',
        )
        prev_btn.add_css_class(css_class='circular')
        controls_box.append(child=prev_btn)

        play_pause_btn = Gtk.Button.new_from_icon_name(
            icon_name='media-playback-pause-symbolic',
        )
        play_pause_btn.add_css_class(css_class='circular')
        play_pause_btn.add_css_class(css_class='suggested-action')
        controls_box.append(child=play_pause_btn)

        next_btn = Gtk.Button.new_from_icon_name(
            icon_name='media-skip-forward-symbolic',
        )
        next_btn.add_css_class(css_class='circular')
        controls_box.append(child=next_btn)

        repeat_btn = Gtk.Button.new_from_icon_name(
            icon_name='media-playlist-repeat-symbolic',
        )
        repeat_btn.add_css_class(css_class='circular')
        controls_box.append(child=repeat_btn)

        button_close_sheet = Gtk.Button(label='Close')
        button_close_sheet.add_css_class(css_class='destructive-action')
        button_close_sheet.connect(
            'clicked', self.on_button_close_sheet_clicked
        )
        button_close_sheet.set_margin_top(margin=12)
        sheet_box.append(child=button_close_sheet)

    def on_play_button_clicked(self, button):
        current_state = self.adw_bottom_sheet.get_open()
        self.adw_bottom_sheet.set_open(open=not current_state)

    def on_button_close_sheet_clicked(self, button):
        """Fecha o painel"""
        self.adw_bottom_sheet.set_open(open=False)


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
