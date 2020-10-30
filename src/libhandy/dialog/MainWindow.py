# -*- coding: utf-8 -*-
"""Handy.Dialog()."""

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Handy', '0.0')

from gi.repository import Gtk, Gio
from gi.repository import Handy


class MainWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Configurando a janela principal.
        self.set_title(title='Handy.Dialog')
        self.set_default_size(width=1366 / 2, height=768 / 2)
        self.set_position(position=Gtk.WindowPosition.CENTER)
        self.set_default_icon_from_file(filename='../../assets/icons/icon.png')

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_border_width(border_width=12)
        self.add(widget=vbox)

        # Botão que ira abrir a janela de dialogo
        button_open_dialog = Gtk.Button.new_with_label(
            label='Abrir janela de dialogo'
        )
        button_open_dialog.connect('clicked', self.open_dialog)
        vbox.add(widget=button_open_dialog)

        self.show_all()

    def open_dialog(self, button):
        hdy_dialog = HdyDialog(parent=self)

        response = hdy_dialog.run()

        # Verificando qual botão foi pressionado.
        if response == Gtk.ResponseType.YES:
            print('Botão SIM pressionado')
            print(f'Valor do Gtk.Entry = {hdy_dialog.get_entry_value()}')

        elif response == Gtk.ResponseType.NO:
            print('Botão NÃO pressionado')

        else:
            print('Botão de FECHAR pressionado')

        # Fechando a janela de diálogo.
        hdy_dialog.destroy()


class HdyDialog(Handy.Dialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.set_title(title='Diálogo com libhandy')
        self.add_buttons(
            '_Não', Gtk.ResponseType.NO,
            '_Sim', Gtk.ResponseType.YES,
        )

        btn_yes = self.get_widget_for_response(
            response_id=Gtk.ResponseType.YES,
        )
        btn_yes.get_style_context().add_class(class_name='suggested-action')

        # Adicionando class action nos botões.
        btn_no = self.get_widget_for_response(
            response_id=Gtk.ResponseType.NO,
        )
        btn_no.get_style_context().add_class(class_name='destructive-action')

        # Acessando a área de conteúdo da janela de dialogo para poder
        # adicionar novos widgets dentro dessa área.
        content_area = self.get_content_area()
        content_area.set_border_width(border_width=12)
        content_area.set_spacing(spacing=12)

        # Criando widgets que serão adicionados na janela de dialogo.
        label = Gtk.Label.new(str='Valor do entry será exibido no terminal.')
        content_area.add(widget=label)

        self.entry = Gtk.Entry.new()
        self.entry.set_placeholder_text(text='Digite algo e clique em sim')
        content_area.add(widget=self.entry)

        # É obrigatório utilizar ``show_all()``, caso contrário
        # ``get_content_area()`` não exibe os widgets.
        self.show_all()

    def get_entry_value(self):
        return self.entry.get_text()


class Application(Gtk.Application):

    def __init__(self):
        super().__init__(application_id='br.natorsc.Exemplo',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)


if __name__ == '__main__':
    import sys

    app = Application()
    app.run(sys.argv)