# Como criar um aplicativo com Python e GTK no macOS

Este guia descreve como preparar seu ambiente de desenvolvimento no macOS para criar aplicações utilizando a linguagem de programação [Python](https://www.python.org/) ([PyGObject](https://pypi.org/project/PyGObject/)) e o toolkit gráfico [GTK](https://www.gtk.org/).

Preparar o ambiente de desenvolvimento no macOS é um processo direto. Na maioria dos casos, todos os pacotes necessários estão disponíveis através do [Homebrew](https://brew.sh/).

## Instalação

Os comandos a seguir permitirão a execução do binding PyGObject tanto na instalação local do Python quanto em um ambiente virtual (recomendado).

```bash
brew install \
python@3.12 \
pygobject3 \
adwaita-icon-theme \
libadwaita \
gtk4
```

## Ambientes Virtuais

Se você ainda não os utiliza, este é um bom momento para explorar algumas opções:

  * [Poetry](https://python-poetry.org/)
  * [Pipenv](https://pipenv.pypa.io/en/latest/)
  * [Pyenv](https://github.com/pyenv/pyenv)
  * [PDM](https://pdm.fming.dev/)
  * [venv](https://docs.python.org/3/library/venv.html) (nativo)
  * Outros

### Criando um Ambiente Virtual

Acesse a pasta raiz do seu projeto, abra um terminal e execute o seguinte comando:

```bash
python3 -m venv venv
```

Para criar um ambiente virtual utilizando uma **versão específica** da linguagem Python, você pode usar o comando:

```bash
python3.X -m venv venv
```

> ⚠️ Substitua `X` pela versão do Python que você deseja utilizar.
> ⚠️ A versão desejada deve estar instalada no seu sistema operacional\!

### Ativando o Ambiente Virtual

Após a criação, o ambiente virtual **precisa ser ativado**. Caso contrário, os pacotes serão instalados na sua instalação global do Python, e não no ambiente virtual.

Para ativar o ambiente virtual:

```bash
source venv/bin/activate
```

### Instalando o Binding

**Com o ambiente virtual ativo**, comece atualizando o gerenciador de pacotes do Python (`pip`) com o comando:

```bash
python -m pip install \
--upgrade pip
```

Em seguida, instale o binding `PyGObject` e a biblioteca `PyGObject-stubs` com o comando:

```bash
pip install \
pygobject \
PyGObject-stubs
```

Com isso, você pode iniciar o desenvolvimento em um ambiente com dependências isoladas.

## Testando

A maneira mais simples de testar a comunicação entre a linguagem de programação Python e o toolkit gráfico GTK é executar o seguinte comando no terminal:

```bash
python3 -c "import gi"
```

> ⚠️ Lembre-se que o comando deve ser executado com o ambiente virtual ativo\!

Se nenhum erro for retornado após a execução do comando, a instalação e configuração estão corretas.

## Código de Exemplo

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
