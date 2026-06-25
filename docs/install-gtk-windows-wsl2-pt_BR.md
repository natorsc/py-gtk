# Como criar um aplicativo com Python e GTK no Windows WSL 2

Como preparar o ambiente de desenvolvimento para criar aplicativos com a linguagem de programação [Python](https://www.python.org/) ([PyGObject](https://pypi.org/project/PyGObject/)) e o *toolkit* gráfico [GTK](https://www.gtk.org/) no [WSL](https://learn.microsoft.com/pt-br/windows/wsl/about) 2 (Windows Subsystem for Linux) do Microsoft Windows.

Através do [WSLg](https://github.com/microsoft/wslg) (Windows Subsystem for Linux GUI), é possível iniciar e interagir com aplicativos gráficos do Linux usando um ambiente de *desktop* nativo do Windows.

O WSLg utiliza o protocolo de servidor de exibição [Wayland](https://wayland.freedesktop.org/) e um compositor de sistema do Windows para renderizar os aplicativos GUI do Linux. Ele também aproveita a aceleração da GPU para melhorar o desempenho gráfico.

> ⚠️ Para utilizar o WSLg, é necessário possuir o Microsoft Windows 10 **Build 19044** ou superior.

## Instalando o WSL

A instalação do WSL 2 é bastante simples.

Abra o PowerShell ou CMD **como administrador** e execute o comando:

```ps1
wsl --install
```

Assim que o comando finalizar a instalação de todos os componentes do WSL 2 e da distribuição Linux [Ubuntu](https://ubuntu.com/download), **reinicie o computador**.

## Dependências

Localize a distribuição Linux Ubuntu no menu iniciar do Microsoft Windows.

> ⚠️ Na primeira execução, será solicitada a criação de um usuário e senha.

Assim que o Ubuntu estiver inicializado, digite no terminal:

```bash
sudo apt update && sudo apt dist-upgrade
```

Após a conclusão das atualizações, instale a linguagem de programação Python e as bibliotecas do GTK com o comando:

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

Ao finalizar a instalação dos pacotes, a linguagem de programação Python, o *binding* `PyGObject` e as bibliotecas do GTK estarão instalados e prontos para uso 🚀.

## Visual Studio Code

O [Visual Studio Code](https://code.visualstudio.com/) possui o *plugin* [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl).

Esse *plugin* permite a interação do editor de texto Visual Studio Code com o WSL 2.

### Código de exemplo

> ⚠️ É possível utilizar o Explorador de Arquivos do Microsoft Windows para gerenciar as pastas e arquivos que estão dentro do WSL 2.

Para testar a configuração, crie um arquivo e digite o seguinte código:

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

> ⚠️ É importante notar que o código não está rodando de forma nativa no Microsoft Windows, mas sim, sendo executado no Linux e exibido no Windows.
