# Como criar um aplicativo com Python e GTK no MS Windows

Hoje veremos como preparar o ambiente de desenvolvimento para a criação de aplicativos com a linguagem de programação [Python](https://www.python.org/) ([PyGObject](https://pypi.org/project/PyGObject/)) e o toolkit gráfico [GTK](https://www.gtk.org/) no Microsoft Windows.

## MSYS2

O [MSYS2](https://www.msys2.org/) permite que pacotes, ferramentas e bibliotecas do Linux sejam instalados e executados de forma nativa no Microsoft Windows.

Para a instalação e gestão dos pacotes, o MSYS2 utiliza o gerenciador de pacotes [Pacman](https://pt.wikipedia.org/wiki/Pacman_\(gerenciador_de_pacotes\)).

### Instalação

A instalação do MSYS2 é **muito** simples.

Antes de mais nada, acesse o site oficial [https://www.msys2.org/](https://www.msys2.org/) e realize o download do instalador.

Assim que o download for concluído, **dê dois cliques** sobre o instalador que foi baixado.

O instalador é **muito** simples e não é necessário alterar as configurações padrão que são exibidas nas telas.

Clique em **Next** e avance até finalizar a instalação.

Com o fim da instalação, procure pelo **terminal** do MSYS2 no **menu Iniciar** do Microsoft Windows.

Com o terminal aberto, realize a atualização dos pacotes que **vêm** instalados:

```bash
pacman -Syu
````

Assim que as atualizações estiverem finalizadas, **pode ser** necessário fechar e abrir o terminal novamente.

## GTK

O comando exibido **nesta seção** irá instalar as bibliotecas do GTK, a linguagem de programação [Python](https://www.python.org/) e o binding [PyGObject](https://pypi.org/project/PyGObject/).

### Dependências

> 🚨 Os comandos abaixo devem ser executados no **terminal do MSYS2**\!

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

Após instalar as **dependências**, precisamos adicionar algumas **pastas** ao PATH do sistema operacional.

1.  Acesse as configurações (`settings`) -\> pesquise (`Search`) pelo aplicativo "Configurações avançadas do sistema" (`Advanced system settings`) -\> clique em "Variáveis de ambiente" (`Environment variables`).

2.  selecione (`Path`) -\> e clique em "Editar" (`Edit`) -\> Adicione os seguintes caminhos:

    ```plaintext
    C:\msys64\mingw64\include
    C:\msys64\mingw64\bin
    C:\msys64\mingw64\lib
    ```

Após configurar os diretórios acima nas variáveis de ambiente do Microsoft Windows, abra o terminal `MinGW x64` e digite:

```bash
python3 -c "import gi"
```

> ⚠️ Não é o terminal do MSYS2, mas sim o terminal `MinGW x64`.

Para testar via **PowerShell** ou outros terminais:

```bash
C:\msys64\mingw64\bin\python3 -c "import gi"
```

Se ao executar o comando nenhum erro for retornado, a instalação e configuração estão corretas 👍👋👋.

## Código de exemplo

Para testar a configuração, crie um arquivo e digite o seguinte código **nele**:

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

    def __init__(self, **kwargs):
        super().__init__(application_id='br.com.justcode.Example',
                         flags=Gio.ApplicationFlags.FLAGS_NONE,
                         **kwargs) # Adicionado **kwargs para consistência

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
        print('Ação app.preferences foi ativada.') # Corrigido para "ativada"

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
