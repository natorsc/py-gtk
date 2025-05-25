# -*- coding: utf-8 -*-
"""Collecting widget information."""

import pathlib

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, GObject, Gtk

BASE_DIR = pathlib.Path(__file__).resolve().parent
TEMPLATE_FILE = BASE_DIR / 'templates' / 'widget.md'
OUTPUT_DIR = BASE_DIR / 'widgets-info'
if not OUTPUT_DIR.exists():
    OUTPUT_DIR.mkdir()

PYGOBJECT_VERSION = GObject.pygobject_version
GTK_VERSION = (
    Gtk.get_major_version(),
    Gtk.get_minor_version(),
    Gtk.get_micro_version(),
)
LIBADWAITA_VERSION = (
    Adw.get_major_version(),
    Adw.get_minor_version(),
    Adw.get_micro_version(),
)


data = open(file=TEMPLATE_FILE, mode='r', encoding='utf-8')
template = data.read()

print('[!] Collecting information, please wait... [!]')
WIDGETS = [Gtk.Button(), Adw.ActionRow()]
for widget in WIDGETS:
    widget_name = widget.get_name()
    methods_get = [
        method for method in dir(widget) if method.startswith('get_')
    ]
    methods_set = [
        method for method in dir(widget) if method.startswith('set_')
    ]

    output = OUTPUT_DIR.joinpath(f'{widget_name}.md')
    output.write_text(
        encoding='utf-8',
        data=template.format(
            widget_name=widget_name,
            gtk_version=GTK_VERSION,
            libadwaita_version=LIBADWAITA_VERSION,
            pygobject_version=PYGOBJECT_VERSION,
            widget_props='\n- '.join(sorted(dir(widget.props))),
            widget_signals='\n- '.join(
                sorted(GObject.signal_list_names(widget))
            ),
            methods_get='\n- '.join(sorted(methods_get)),
            methods_set='\n- '.join(sorted(methods_set)),
        ),
    )
print('[!] Finished [!]')
