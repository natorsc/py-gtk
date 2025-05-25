# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib

import gi

gi.require_version(namespace='Gtk', version='4.0')


from gi.repository import Gio, Gtk, Pango, PangoCairo

BASE_DIR = pathlib.Path(__file__).resolve().parent
PDF_FILE = str(BASE_DIR / 'file-name.pdf')

TEXT = """<span size="xx-large">Lorem</span>
Lorem <b>ipsum</b> <span foreground="red">dolor</span> <big>sit</big> amet,
<i>consectetur</i> adipiscing <s>elit</s>, sed do 
<span background="green">eiusmod</span> tempor incididunt 
<small>ut</small> <tt>labore</tt> et dolore magna aliqua.\n"""


class ExampleWindow(Gtk.ApplicationWindow):
    pango_layout = None

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

        # Auxiliary variable with paper settings.
        self.page_setup = self._page_setup()
        # self.page_setup = self.custom_page_setup()

        # Variable for the paper configuration dialog:
        self.print_settings = Gtk.PrintSettings.new()

        # Text buffer.
        self.text_buffer = Gtk.TextBuffer.new()

        # Adding rendered text to Gtk.TextView.
        text_buffer_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert_markup(
            iter=text_buffer_iter,
            markup=TEXT,
            len=-1,
        )

        text_view = Gtk.TextView.new_with_buffer(buffer=self.text_buffer)
        text_view.set_vexpand(expand=True)
        vbox.append(child=text_view)

        hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        hbox.set_halign(align=Gtk.Align.CENTER)
        vbox.append(child=hbox)

        button_print_dialog = Gtk.Button.new_with_label(label='Print')
        button_print_dialog.connect(
            'clicked',
            self.on_button_open_print_dialog_clicked,
        )
        hbox.append(child=button_print_dialog)

        button_open_preview = Gtk.Button.new_with_label(label='View')
        button_open_preview.connect(
            'clicked',
            self.on_button_open_preview_clicked,
        )
        hbox.append(child=button_open_preview)

        button_page_setup_dialog = Gtk.Button.new_with_label(
            label='Page setup'
        )
        button_page_setup_dialog.connect(
            'clicked',
            self.on_button_open_page_setup_dialog_clicked,
        )
        hbox.append(child=button_page_setup_dialog)

        button_export_pdf = Gtk.Button.new_with_label('Export to PDF')
        button_export_pdf.connect(
            'clicked',
            self.on_button_export_to_pdf_clicked,
        )
        hbox.append(child=button_export_pdf)

    def on_begin_print(self, print_operation, print_context):
        font_description = Pango.FontDescription.new()
        font_description.set_family(family='Adwaita')

        self.pango_layout = print_context.create_pango_layout()
        self.pango_layout.set_markup(text=TEXT, length=-1)
        self.pango_layout.set_font_description(
            desc=font_description,
        )

    def on_draw_page(self, print_operation, print_context, page_nr):
        cairo_context = print_context.get_cairo_context()
        cairo_context.set_source_rgb(0, 0, 0)
        PangoCairo.show_layout(cr=cairo_context, layout=self.pango_layout)

    def on_button_open_print_dialog_clicked(self, widget):
        print_operation = Gtk.PrintOperation.new()
        print_operation.set_n_pages(n_pages=1)
        print_operation.set_print_settings(print_settings=self.print_settings)
        print_operation.set_default_page_setup(
            default_page_setup=self.page_setup
        )
        print_operation.connect('begin-print', self.on_begin_print)
        print_operation.connect('draw-page', self.on_draw_page)

        response = print_operation.run(
            parent=self,
            action=Gtk.PrintOperationAction.PRINT_DIALOG,
        )
        self._check_print_dialog_response(response=response)

    def on_button_open_preview_clicked(self, widget):
        print_operation = Gtk.PrintOperation.new()
        print_operation.set_n_pages(n_pages=1)
        print_operation.set_print_settings(print_settings=self.print_settings)
        print_operation.set_default_page_setup(
            default_page_setup=self.page_setup
        )
        print_operation.connect('begin-print', self.on_begin_print)
        print_operation.connect('draw-page', self.on_draw_page)

        response = print_operation.run(
            action=Gtk.PrintOperationAction.PREVIEW, parent=self
        )
        self._check_print_dialog_response(response=response)

    def on_button_open_page_setup_dialog_clicked(self, widget):
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))
        self.page_setup = Gtk.print_run_page_setup_dialog(
            parent=self,
            page_setup=self.page_setup,
            settings=self.print_settings,
        )
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))

    def on_button_export_to_pdf_clicked(self, widget):
        print_operation = Gtk.PrintOperation.new()
        print_operation.set_n_pages(n_pages=1)
        print_operation.set_print_settings(print_settings=self.print_settings)
        print_operation.set_default_page_setup(
            default_page_setup=self.page_setup
        )
        print_operation.connect('begin-print', self.on_begin_print)
        print_operation.connect('draw-page', self.on_draw_page)
        print_operation.set_export_filename(PDF_FILE)
        response = print_operation.run(
            action=Gtk.PrintOperationAction.EXPORT, parent=self
        )
        if response == Gtk.PrintOperationResult.APPLY:
            print('Arquivo exportado com sucesso')

    def _page_setup(self):
        paper_size = Gtk.PaperSize.new(name=Gtk.PAPER_NAME_A4)
        page_setup = Gtk.PageSetup.new()
        page_setup.set_paper_size_and_default_margins(size=paper_size)
        return page_setup

    def _custom_page_setup(self):
        paper_size = Gtk.PaperSize.new(name=Gtk.PAPER_NAME_A4)
        custom_page_setup = Gtk.PageSetup.new()
        custom_page_setup.set_top_margin(margin=20, unit=Gtk.Unit.MM)
        custom_page_setup.set_left_margin(margin=20, unit=Gtk.Unit.MM)
        custom_page_setup.set_orientation(
            orientation=Gtk.PageOrientation.PORTRAIT,
        )
        custom_page_setup.set_paper_size(size=paper_size)
        return custom_page_setup

    def _check_print_dialog_response(self, response):
        if response == Gtk.PrintOperationResult.ERROR:
            print('ERROR')
        elif response == Gtk.PrintOperationResult.APPLY:
            print('APPLY')
        elif response == Gtk.PrintOperationResult.CANCEL:
            print('CANCEL')
        elif response == Gtk.PrintOperationResult.IN_PROGRESS:
            print('IN_PROGRESS')


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
