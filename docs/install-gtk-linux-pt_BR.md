# Como criar um aplicativo com Python e GTK no Linux

Para preparar o ambiente de desenvolvimento para a criação de aplicativos com a linguagem de programação [Python](https://www.python.org/) ([PyGObject](https://pypi.org/project/PyGObject/)) e o toolkit gráfico [GTK](https://www.gtk.org/) no Linux.

Preparar o ambiente de desenvolvimento em distribuições Linux é bem simples. Na maioria dos casos, todos os pacotes necessários estão nos repositórios e podem ser instalados por meio do gerenciador de pacotes da distribuição.

É importante notar que, **atualmente**, a melhor forma de iniciar um novo projeto GTK é utilizando o IDE [Gnome Builder](https://wiki.gnome.org/Apps/Builder) juntamente com o sistema de empacotamento/distribuição [Flatpak](https://flatpak.org/) 💜.

## Instalação

Os comandos a seguir permitirão a execução do *binding* PyGObject na instalação local do Python, bem como sua utilização em um ambiente virtual (recomendado).

### Arch Linux

Site oficial da distribuição Linux [Arch Linux](https://archlinux.org/).

#### Dependências

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

Site oficial da distribuição Linux [Fedora](https://getfedora.org/).

#### Dependências

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

Site oficial da distribuição Linux [openSUSE Tumbleweed](https://get.opensuse.org/tumbleweed/).

#### Dependências

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

Site oficial da distribuição Linux [Ubuntu](https://ubuntu.com/).

#### Dependências

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

Ao finalizar a instalação dos pacotes, a linguagem de programação Python, o *binding* `PyGObject` e as bibliotecas do GTK estarão instalados e prontos para uso 🚀.

## Ambientes virtuais

Se você ainda não os utiliza, este é um bom momento para testar algumas opções:

  * [Poetry](https://python-poetry.org/).
  * [Pipenv](https://pipenv.pypa.io/en/latest/).
  * [Pyenv](https://github.com/pyenv/pyenv).
  * [PDM](https://pdm.fming.dev/).
  * [venv](https://docs.python.org/3/library/venv.html). Nativo.
  * Etc.

### Criando o ambiente virtual

Acesse a pasta raiz do seu projeto, abra um terminal e execute o comando:

```bash
python3 -m venv venv
```

Para criar o ambiente virtual utilizando uma **versão específica** da linguagem de programação Python, pode ser utilizado o comando:

```bash
python3.X -m venv venv
```

> ⚠️ Substitua o `X` pela versão da linguagem de programação Python que deseja utilizar.

> ⚠️ A versão desejada deve estar instalada no sistema operacional\!

### Ativando o ambiente virtual

Após ser criado, o ambiente virtual **precisa ser ativado**. Caso contrário, a instalação dos pacotes será realizada na instalação local da linguagem de programação Python e não no ambiente virtual.

Para ativar o ambiente virtual:

```bash
source venv/bin/activate
```

### Instalando o *binding*

**Com o ambiente virtual ativo**, vamos começar atualizando o gerenciador de pacotes do Python (`pip`) com o comando:

```bash
python -m pip install \
--upgrade pip
```

Em seguida, instalaremos o *binding* `PyGObject` e a biblioteca `PyGObject-stubs` com o comando:

```bash
pip install \
pygobject \
PyGObject-stubs
```

Perfeito\! Com isso, podemos iniciar o desenvolvimento em um ambiente onde as dependências estão isoladas 😃.

## Testando

A forma mais simples de testar a comunicação entre a linguagem de programação Python e o *toolkit* gráfico GTK é executar no terminal o comando:

```bash
python3 -c "import gi"
```

> ⚠️ Lembre-se que o comando deve ser executado com o ambiente virtual ativo\!

Se ao executar o comando nenhum erro for retornado, a instalação e a configuração estão corretas 👍👋👋.

## Código de exemplo

Para testar a configuração no seu editor de texto ou IDE, utilize o seguinte código de exemplo:

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
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        # O seu código aqui:
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
        print('Ação app.preferences foi ativa.')

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
