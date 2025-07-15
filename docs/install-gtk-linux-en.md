# How to create a Python and GTK Application on Linux

To prepare your development environment for creating applications with the [Python](https://www.python.org/) programming language ([PyGObject](https://pypi.org/project/PyGObject/)) and the [GTK](https://www.gtk.org/) graphical toolkit on Linux.

Setting up the development environment on Linux distributions is quite simple. In most cases, all necessary packages are available in the repositories and can be installed via the distribution's package manager.

It's important to note that, **currently**, the best way to start a new GTK project is by using the [Gnome Builder](https://wiki.gnome.org/Apps/Builder) IDE along with the [Flatpak](https://flatpak.org/) packaging/distribution system 💜.

## Installation

The following commands will enable the execution of the PyGObject binding in your local Python installation, as well as its use in a virtual environment (recommended).

### Arch Linux

Official website of the [Arch Linux](https://archlinux.org/) distribution.

#### Dependencies

```bash
sudo pacman -S \
python \
python-pip \
cairo \
pkgconf \
gobject-introspection \
gtk4 \
libadwaita \
blueprint-compiler
````

### Fedora

Official website of the [Fedora](https://getfedora.org/) distribution.

#### Dependencies

```bash
sudo dnf install \
python3 \
python3-devel \
python3-gobject \
gcc \
pkg-config \
cairo-devel \
cairo-gobject-devel \
gobject-introspection-devel \
gtk4 \
gtk4-devel \
gtk4-devel-tools \
libadwaita-devel \
blueprint-compiler
```

### openSUSE Tumbleweed

Official website of the [openSUSE Tumbleweed](https://get.opensuse.org/tumbleweed/) distribution.

#### Dependencies

```bash
sudo zypper install \
python311-devel \
python311-gobject \
python311-gobject-Gdk \
gcc \
pkgconf-pkg-config \
cairo-devel \
gobject-introspection-devel \
libgtk-4-1 \
gtk4-devel \
gtk4-tools \
libadwaita-devel
```

### Ubuntu

Official website of the [Ubuntu](https://ubuntu.com/) distribution.

#### Dependencies

```bash
sudo apt install \
python3-full \
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

Upon completing the package installation, the Python programming language, the `PyGObject` binding, and the GTK libraries will be installed and ready for use 🚀.

## Virtual Environments

If you are not already using them, this is a good time to explore some options:

  * [Poetry](https://python-poetry.org/).
  * [Pipenv](https://pipenv.pypa.io/en/latest/).
  * [Pyenv](https://github.com/pyenv/pyenv).
  * [PDM](https://pdm.fming.dev/).
  * [venv](https://docs.python.org/3/library/venv.html). Native.
  * Etc.

### Creating the Virtual Environment

Navigate to your project's root folder, open a terminal, and then execute the command:

```bash
python3 -m venv venv
```

To create a virtual environment using a **specific version** of the Python programming language, you can use the command:

```bash
python3.X -m venv venv
```

> ⚠️ Replace `X` with the desired Python version.

> ⚠️ The desired version must be installed on your operating system\!

### Activating the Virtual Environment

After creation, the virtual environment **needs to be activated**. Otherwise, packages will be installed in the local Python installation and not within the virtual environment.

To activate the virtual environment:

```bash
source venv/bin/activate
```

### Installing the Binding

**With the virtual environment active**, let's start by updating Python's package manager (`pip`) with the command:

```bash
python -m pip install \
--upgrade pip
```

Next, we will install the `PyGObject` binding and the `PyGObject-stubs` library with the command:

```bash
pip install \
pygobject \
PyGObject-stubs
```

Perfect\! With this, we can begin development in an environment where dependencies are isolated 😃.

## Testing

The simplest way to test the communication between the Python programming language and the GTK graphical toolkit is to execute the following command in the terminal:

```bash
python3 -c "import gi"
```

> ⚠️ Remember that the command must be executed with the virtual environment active\!

If no errors are returned when executing the command, the installation and configuration are correct 👍👋👋.

## Example Code

To test the configuration in your text editor or IDE, use the following example code:

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
