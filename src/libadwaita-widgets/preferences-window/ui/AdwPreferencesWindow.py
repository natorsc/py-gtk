# -*- coding: utf-8 -*-
"""Python - GTK - PyGObject."""

import pathlib
import sys

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
UI = BASE_DIR.joinpath('AdwPreferencesWindow.ui')


Adw.init()


@Gtk.Template(filename=UI)
class AdwPreferencesWindow(Adw.PreferencesWindow):
    __gtype_name__ = 'PreferencesWindow'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # @Gtk.Template.Callback()
    # def on_button_clicked(self, button):
    #     if 'background' in self.button.get_css_classes():
    #         self.button.remove_css_class(css_class='background')
    #     else:
    #         self.button.add_css_class(css_class='background')
