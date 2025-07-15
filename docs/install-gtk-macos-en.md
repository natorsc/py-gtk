# How to create a Python and GTK Application on macOS

## Setting Up Your Development Environment for Python Applications with GTK on macOS

This guide outlines how to set up your development environment on macOS to create applications using the [Python](https://www.python.org/) programming language ([PyGObject](https://pypi.org/project/PyGObject/)) and the [GTK](https://www.gtk.org/) graphical toolkit.

Setting up your development environment on macOS is a straightforward process. In most cases, all necessary packages are readily available through [Homebrew](https://brew.sh/).

### Installation

The following commands will enable the PyGObject binding to run both within your local Python installation and, as recommended, within a virtual environment.

```bash
brew install \
python@3.12 \
pygobject3 \
adwaita-icon-theme \
libadwaita \
gtk4
```

## Virtual Environments

If you don't already use them, now is an excellent time to explore some options:

  * [Poetry](https://python-poetry.org/)
  * [Pipenv](https://pipenv.pypa.io/en/latest/)
  * [Pyenv](https://github.com/pyenv/pyenv)
  * [PDM](https://pdm.fming.dev/)
  * [venv](https://docs.python.org/3/library/venv.html) (Native)
  * And others

### Creating a Virtual Environment

Navigate to your project's root folder, open a terminal, and then execute the following command:

```bash
python3 -m venv venv
```

To create a virtual environment using a **specific version** of the Python programming language, you can use the command:

```bash
python3.X -m venv venv
```

> ⚠️ Replace `X` with the Python version you wish to use.
> ⚠️ The desired version must already be installed on your operating system\!

### Activating the Virtual Environment

Once created, the virtual environment **must be activated**. Otherwise, packages will be installed into your global Python installation instead of the virtual environment.

To activate the virtual environment:

```bash
source venv/bin/activate
```

### Installing the Binding

**With the virtual environment active**, begin by upgrading Python's package manager (`pip`) using the command:

```bash
python -m pip install \
--upgrade pip
```

Next, install the `PyGObject` binding and the `PyGObject-stubs` library with the command:

```bash
pip install \
pygobject \
PyGObject-stubs
```

With these steps complete, you can now begin development in an environment with isolated dependencies.

## Testing

The simplest way to test the communication between the Python programming language and the GTK graphical toolkit is to execute the following command in your terminal:

```bash
python3 -c "import gi"
```

> ⚠️ Remember that this command must be executed with the virtual environment active\!

If no errors are returned after executing the command, your installation and configuration are correct.

## Example Code

To test your setup in your text editor or IDE, use the following example code:

```python
# -*- coding: utf-8 -*-
"""Python - PyGObject - GTK."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python - PyGObject - GTK')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferences', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        # Your code here:
        # ...


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

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
        print('app.preferences action was activated.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
```
