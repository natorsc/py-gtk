# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')

from gi.repository import Gio, Gtk, Pango, PangoCairo

BASE_DIR = pathlib.Path(__file__).resolve().parent
BLP_FILE = BASE_DIR / 'MainWindow.blp'
UI_FILE = BASE_DIR / 'MainWindow.ui'
PDF_FILE = str(BASE_DIR / 'file-name.pdf')

TEXT = """<span size="xx-large">Lorem</span>
Lorem <b>ipsum</b> <span foreground="red">dolor</span> <big>sit</big> amet,
<i>consectetur</i> adipiscing <s>elit</s>, sed do 
<span background="green">eiusmod</span> tempor incididunt 
<small>ut</small> <tt>labore</tt> et dolore magna aliqua.\n"""

sys.path.append(str(BASE_DIR.parent.parent.parent / 'scripts'))

from blp import blp_to_ui

blp_to_ui(file=BLP_FILE)


@Gtk.Template(filename=UI_FILE)
class ExampleWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'ExampleWindow'

    pango_layout = None

    text_buffer = Gtk.Template.Child('text_buffer')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Auxiliary variable with paper settings.
        self.page_setup = self._page_setup()
        # self.page_setup = self.custom_page_setup()

        # Variable for the paper configuration dialog:
        self.print_settings = Gtk.PrintSettings.new()

        # Adding rendered text to Gtk.TextView.
        text_buffer_iter = self.text_buffer.get_end_iter()
        self.text_buffer.insert_markup(
            iter=text_buffer_iter,
            markup=TEXT,
            len=-1,
        )

    @Gtk.Template.Callback()
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

    @Gtk.Template.Callback()
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

    @Gtk.Template.Callback()
    def on_button_open_page_setup_dialog_clicked(self, widget):
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))
        self.page_setup = Gtk.print_run_page_setup_dialog(
            parent=self,
            page_setup=self.page_setup,
            settings=self.print_settings,
        )
        print(self.page_setup.get_page_width(unit=Gtk.Unit.MM))

    @Gtk.Template.Callback()
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

    def on_begin_print(self, print_operation, print_context):
        font_description = Pango.FontDescription.new()
        font_description.set_family(family='Adwaita')

        self.pango_layout = print_context.create_pango_layout()
        self.pango_layout.set_markup(text=TEXT, length=-1)
        self.pango_layout.set_font_description(desc=font_description)

    def on_draw_page(self, print_operation, print_context, page_nr):
        cairo_context = print_context.get_cairo_context()
        cairo_context.set_source_rgb(0, 0, 0)
        PangoCairo.show_layout(cr=cairo_context, layout=self.pango_layout)

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
    app = ExampleApplication()
    app.run(sys.argv)
