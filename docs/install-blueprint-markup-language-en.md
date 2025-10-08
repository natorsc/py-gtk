
# How to Install the Gnome Blueprint Markup Language

Blueprint is a markup language for creating graphical user interfaces using the [GTK](https://www.gtk.org/) toolkit.

It is developed and maintained by [James Westman](https://gitlab.gnome.org/jwestman).

Its main goal is to be an easy-to-learn markup language that enables building graphical interfaces quickly and declaratively.

It’s important to note that the Blueprint markup language **does not replace** the current standard for building GTK graphical interfaces, since Blueprint code is compiled/transpiled into XML.

As with other GUI frameworks and toolkits, GTK uses the [XML](https://en.wikipedia.org/wiki/XML) format to define the visual part of applications.

This format is widely used and generally well accepted; however, it tends to be hard to read and modify **manually**.

That difficulty often leads to a steep learning curve, and in many cases, there’s a need for tools that allow visual interface design.

Some examples of such tools are:

* [Cambalache](https://gitlab.gnome.org/jpu/cambalache)
* [Drafting](https://gitlab.gnome.org/chergert/drafting)
* [Glade](https://glade.gnome.org/) — Not recommended for GTK 4 development.
* [Workbench](https://github.com/workbenchdev/Workbench) — A tool for learning and prototyping.

The idea behind the Blueprint markup language emerged to make this process easier.

To better understand it, let’s compare the code for the same graphical interface in both markup languages.

To describe a GTK interface in XML (`*.ui`), you can use the following code:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<interface>
    <requires lib="gtk" version="4.0"/>
    <template class="ExampleWindow" parent="GtkApplicationWindow">
        <property name="title">Python (PyGObject) GTK 4.</property>
        <property name="default-width">683</property>
        <property name="default-height">384</property>
        <child type="titlebar">
            <object class="GtkHeaderBar" id="header_bar">
                <child type="end">
                    <object class="GtkMenuButton">
                        <property name="icon-name">open-menu-symbolic</property>
                        <property name="menu-model">primary_menu</property>
                    </object>
                </child>
            </object>
        </child>
    </template>

    <menu id="primary_menu">
        <section>
            <item>
                <attribute name="label" translatable="yes">_Preferences</attribute>
                <attribute name="action">app.preferences</attribute>
            </item>
        </section>
    </menu>
</interface>
```

The same graphical interface in Blueprint markup language (`*.blp`) looks like this:

```javascript
using Gtk 4.0;

template $ExampleWindow: Gtk.ApplicationWindow {
  title: 'Python and GTK: PyGObject Gtk.ApplicationWindow.';
  default-width: 683;
  default-height: 384;

  [titlebar]
  Gtk.HeaderBar header_bar {
    [end]
    Gtk.MenuButton {
      icon-name: 'open-menu-symbolic';
      menu-model: primary_menu;
    }
  }
}

menu primary_menu {
  section {
    item {
      label: _('Preferences');
      action: 'app.preferences';
    }
  }
}
```

As we can see, the interface code becomes much more readable and simpler with Blueprint markup.

---

## Installation via Repositories

### Linux

#### Arch Linux

Official distribution website: [Arch Linux](https://archlinux.org/)

```bash
sudo pacman -S blueprint-compiler
```

#### Fedora

Official distribution website: [Fedora](https://fedoraproject.org/)

```bash
sudo dnf install blueprint-compiler
```

#### openSUSE Tumbleweed

Official distribution website: [openSUSE Tumbleweed](https://www.opensuse.org/#Tumbleweed)

```bash
sudo zypper install blueprint-compiler
```

#### Ubuntu

Official distribution website: [Ubuntu](https://ubuntu.com/)

```bash
sudo apt install blueprint-compiler
```

### Microsoft Windows

> ⚠️ To install `blueprint-compiler` on Microsoft Windows, [MSYS2](https://www.msys2.org/) must be installed and configured.

Open the MSYS2 terminal and run the following command:

```bash
pacman -S mingw-w64-x86_64-blueprint-compiler
```

---

## Installation from Source

To get the latest version of `blueprint-compiler`, you can install it from its source code.

### Dependencies

#### macOS

```bash
brew install git meson ninja
```

#### Arch Linux

```bash
sudo pacman -S git meson ninja
```

#### Fedora

```bash
sudo dnf install git meson ninja-build
```

#### openSUSE Tumbleweed

```bash
sudo zypper install git meson ninja
```

#### Ubuntu

```bash
sudo apt install git meson ninja-build
```

#### Microsoft Windows

> ⚠️ To install `blueprint-compiler` on Microsoft Windows, [MSYS2](https://www.msys2.org/) must be installed and configured.

Open the MSYS2 terminal and install the following dependencies:

```bash
pacman -S git mingw-w64-x86_64-meson mingw-w64-x86_64-ninja
```

### Installation

Once the dependencies are installed, **open a terminal** and clone the `blueprint-compiler` repository:

```bash
git clone https://gitlab.gnome.org/jwestman/blueprint-compiler.git
```

> ⚠️ On Windows, use the `MINGW64` terminal from MSYS2.

Next, navigate to the cloned folder:

```bash
cd blueprint-compiler
```

Run the following command:

```bash
meson _build
```

Once the **build** process finishes, run:

```bash
ninja -C _build install
```

After installation is complete, `blueprint-compiler` will be available on your system 🚀.

To verify the installation, close the terminal, open it again, and run:

```bash
blueprint-compiler --version
```

---

## Main Commands

To start an interactive setup wizard for a project:

```bash
blueprint-compiler port
```

To convert a `*.blp` file to `*.ui`:

```bash
blueprint-compiler compile MainWindow.blp --output MainWindow.ui
```

To see all available options:

```bash
blueprint-compiler --help
```

---

## Extras

### Extensions

Some text editors support the Blueprint markup language.

Here are the main ones:

- [GNU Emacs (DrBluefall)](https://github.com/DrBluefall/blueprint-mode)
- [Visual Studio Code (Bodil Stokke)](https://marketplace.visualstudio.com/items?itemName=bodil.blueprint-gtk)
- [VIM (thetek42)](https://github.com/thetek42/vim-blueprint-syntax)
- [VIM (gabmus)](https://gitlab.com/gabmus/vim-blueprint/-/tree/master)
