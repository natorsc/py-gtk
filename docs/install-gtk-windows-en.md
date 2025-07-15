# How to Create a Python and GTK Application on MS Windows

Today, we will learn how to set up the development environment for creating applications with the [Python](https://www.python.org/) programming language ([PyGObject](https://pypi.org/project/PyGObject/)) and the [GTK](https://www.gtk.org/) graphical toolkit on Microsoft Windows.

## MSYS2

[MSYS2](https://www.msys2.org/) allows Linux packages, tools, and libraries to be installed and run natively on Microsoft Windows.

For package installation and management, MSYS2 uses the [Pacman](https://en.wikipedia.org/wiki/Pacman_\(package_manager\)) package manager.

### Installation

Installing MSYS2 is very straightforward.

First, access the official website [https://www.msys2.org/](https://www.msys2.org/) and download the installer.

Once the download is complete, **double-click** the downloaded installer.

The installer is very simple, and there's no need to change the default settings displayed on the screens.

Click **Next** and proceed until the installation is finished.

After the installation is complete, search for the MSYS2 **terminal** in the Microsoft Windows **Start menu**.

With the terminal open, update the installed packages:

```bash
pacman -Syu
````

Once the updates are finished, it **may be** necessary to close and reopen the terminal.

## GTK

The command shown in **this section** will install the GTK libraries, the [Python](https://www.python.org/) programming language, and the [PyGObject](https://pypi.org/project/PyGObject/) binding.

### Dependencies

> 🚨 The commands below must be executed in the **MSYS2 terminal**\!

```bash
pacman -S \
mingw-w64-x86_64-python3 \
mingw-w64-x86_64-python3-pip \
mingw-w64-x86_64-python3-gobject \
mingw-w64-x86_64-python-autopep8 \
mingw-w64-x86_64-python-pylint \
mingw-w64-x86_64-python-isort \
mingw-w64-x86_64-python-poetry \
mingw-w64-x86_64-blueprint-compiler \
mingw-w64-x86_64-gtk4 \
mingw-w64-x86_64-libadwaita \
mingw-w64-x86_64-gettext \
mingw-w64-x86_64-libxml2 \
mingw-w64-x86_64-librsvg \
mingw-w64-x86_64-pkgconf \
mingw-w64-x86_64-gcc
```

After installing the **dependencies**, we need to add a few **folders** to the operating system's PATH.

1.  Access `Settings` -\> search for `Advanced system settings` -\> click `Environment variables`.

2.  select `Path` -\> and click `Edit` -\> Add the following paths:

    ```plaintext
    C:\msys64\mingw64\include
    C:\msys64\mingw64\bin
    C:\msys64\mingw64\lib
    ```

After configuring the above directories in the Microsoft Windows environment variables, open the `MinGW x64` terminal and type:

```bash
python3 -c "import gi"
```

> ⚠️ This is not the MSYS2 terminal; it is the `MinGW x64` terminal.

To test via **PowerShell** or other terminals:

```bash
C:\msys64\mingw64\bin\python3 -c "import gi"
```

If no error is returned when executing the command, the installation and configuration are correct 👍👋👋.

## Example Code

To test the configuration, create a file and type the following code **into it**:

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

    def __init__(self, **kwargs):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs) # Added **kwargs for consistency

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
        print('app.preferences action was activated.') # Translated comment

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
