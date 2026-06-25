# How to Create a Python and GTK Application on Windows WSL 2

How to set up a development environment for creating applications with the [Python](https://www.python.org/) programming language ([PyGObject](https://pypi.org/project/PyGObject/)) and the [GTK](https://www.gtk.org/) graphical toolkit on Microsoft Windows' [WSL](https://learn.microsoft.com/en-us/windows/wsl/about) 2 (Windows Subsystem for Linux).

Through [WSLg](https://github.com/microsoft/wslg) (Windows Subsystem for Linux GUI), you can launch and interact with Linux graphical applications using a native Windows desktop environment.

WSLg utilizes the [Wayland](https://wayland.freedesktop.org/) display server protocol and a Windows system compositor to render Linux GUI applications. It also leverages GPU acceleration to improve graphical performance.

> ⚠️ To use WSLg, you must have Microsoft Windows 10 **Build 19044** or higher.

## Installing WSL

Installing WSL 2 is quite straightforward.

Open PowerShell or CMD **as an administrator** and run the command:

```ps1
wsl --install
````

Once the command finishes installing all WSL 2 components and the [Ubuntu](https://ubuntu.com/download) Linux distribution, **restart your computer**.

## Dependencies

Locate the Ubuntu Linux distribution in the Microsoft Windows Start menu.

> ⚠️ The first time you launch it, you will be prompted to create a username and password.

Once Ubuntu has started, type the following in the terminal:

```bash
sudo apt update && sudo apt dist-upgrade
```

After the updates are complete, install the Python programming language and the GTK libraries with the command:

```bash
sudo apt install \
build-essential \
meson \
ninja-build \
python3-full \
python3-dev \
python3-pip \
python3-dev \
python3-gi \
python3-gi-cairo \
libcairo2-dev \
libgirepository1.0-dev \
gir1.2-gtk-4.0 \
libgtk-4-dev \
libadwaita-1-dev \
gtk-4-examples
```

Upon completion of the package installation, the Python programming language, the `PyGObject` binding, and the GTK libraries will be installed and ready for use 🚀.

## Visual Studio Code

[Visual Studio Code](https://code.visualstudio.com/) has the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl).

This extension allows the Visual Studio Code text editor to interact with WSL 2.

### Example Code

> ⚠️ You can use Windows File Explorer to manage folders and files within WSL 2.

To test the configuration, create a file and enter the following code:

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
        print('Action app.preferences was activated.')

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

> ⚠️ It's important to note that the code is not running natively on Microsoft Windows; instead, it is executed on Linux and displayed on Windows.
