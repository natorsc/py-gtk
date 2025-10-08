# Como instalar a linguagem de marcação Gnome Blueprint

Blueprint é uma linguagem de marcação para criação de interfaces gráfica com o toolkit [GTK](https://www.gtk.org/).

Ela é desenvolvida e mantida pelo [James Westman](https://gitlab.gnome.org/jwestman).

O seu principal objeto é ser uma linguagem de marcação fácil de aprender e que permita a construção de interfaces gráficas de forma rápida e declarativa.

É importante notar que a linguagem de marcação Blueprint **não vem para substituir o padrão atual** de construção de interfaces gráficas do GTK, visto que o código blueprint será compilado/transpilado para XML.

Assim como em outros frameworks e toolkits gráficos, o GTK utiliza o padrão [XML](https://pt.wikipedia.org/wiki/XML) para construção da parte visual dos aplicativos.

Este é um formato amplamente utilizado e bem aceito no geral, contudo ele tende a ser difícil de ler e modificar **manualmente**.

Essa dificuldade tente a gerar uma curva de aprendizado grande e em muitos casos existe a necessidade da utilização de softwares que permitam o desenvolvimento das interfaces gráficas de forma visual.

Alguns exemplos desses softwares são:

* [Cambalache](https://gitlab.gnome.org/jpu/cambalache).
* [Drafting](https://gitlab.gnome.org/chergert/drafting).
* [Glade](https://glade.gnome.org/). Não é recomendada a sua utilização para o desenvolvimento com GTK 4.
* [Workbench](https://github.com/workbenchdev/Workbench). Ferramenta para estudo e prototipação.

Para amenizar essas dificuldades é que nasce a ideia da linguagem de marcação Blueprint.

Para ficar mais claro vamos analisar o código da seguinte interface gráfica em ambas as linguagens de marcação.

Para descrever uma interface em GTK com XML (`*.ui`) podemos utilizar o seguinte código:

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

A mesma interface gráfica na linguagem de marcação Blueprint (`*.blp`) tem o seguinte código:

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

Como podemos ver o código da interface gráfica se torna bem mais legível e simples com a linguagem de marcação Blueprint.

---

## Instalação via repositórios

### Linux

#### Arch Linux

- Site oficial da distribuição Linux [Arch Linux](https://archlinux.org/).

```bash
sudo pacman -S \
blueprint-compiler
```

#### Fedora

* Site oficial da distribuição Linux [Fedora](https://fedoraproject.org/).

```bash
sudo dnf install \
blueprint-compiler
```

#### openSUSE Tumbleweed

* Site oficial da distribuição Linux [openSUSE Tumbleweed](https://www.opensuse.org/#Tumbleweed).

```bash
sudo zypper install \
blueprint-compiler
```

#### Ubuntu

* Site oficial da distribuição Linux [Ubuntu](https://ubuntu.com/).

```bash
sudo apt install \
blueprint-compiler
```

### Microsoft Windows

> ⚠️ Para realizar a instalação do `blueprint-compiler` no Microsoft Windows é necessário que o [MSYS2](https://www.msys2.org/) esteja instalado e configurado.

Abra o terminal do MSYS2 e execute no terminal o comando:

```bash
pacman -S \
mingw-w64-x86_64-blueprint-compiler
```

---

## Instalação via código fonte

Para obter a ultima versão do `blueprint-compiler` podemos realizar a instalação do mesmo a partir do seu código fonte.

### Dependências

#### macOS

```bash
brew install \
git \
meson \
ninja
```

#### Arch Linux

```bash
sudo pacman -S \
git \
meson \
ninja
```

#### Fedora

```bash
sudo dnf install \
git \
meson \
ninja-build
```

#### openSUSE Tumbleweed

```bash
sudo zypper install \
git \
meson \
ninja
```

#### Ubuntu:

```bash
sudo apt install \
git \
meson \
ninja-build
```

#### Microsoft Windows

> ⚠️ Para realizar a instalação do `blueprint-compiler` no Microsoft Windows é necessário que o [MSYS2](https://www.msys2.org/) esteja instalado e configurado.

Abra o terminal do MSYS2 e instale as seguinte dependências:

```bash
pacman -S \
git \
mingw-w64-x86_64-meson \
mingw-w64-x86_64-ninja
```

### Instalação

Assim que as dependências estiverem instaladas **abra um terminal** e clone o repositório do `blueprint-compiler`:

```bash
git clone https://gitlab.gnome.org/jwestman/blueprint-compiler.git
```

> ⚠️ No caso do Microsoft Windows utilize o terminal `MINGW64` do MSYS2.

Agora acesse a pasta que foi clonada:

```bash
cd blueprint-compiler
```

Ao acessar a pasta execute o comando:

```bash
meson _build
```

Assim que o processo de **build** terminar execute:

```bash
ninja -C _build install
```

Assim que o processo de instalação terminar o `blueprint-compiler` estará disponível no sistema operacional 🚀.

Para testar a instalação feche o terminal, abra novamente e execute:

```bash
blueprint-compiler --version
```

---

## Principais comandos

Iniciar um passo a passo para configuração do projeto:

```bash
blueprint-compiler port
```

Para converter um arquivo `*.blp` para `*.ui`:

```bash
blueprint-compiler compile MainWindow.blp --output MainWindow.ui
```

Para conhecer todos os recursos disponíveis:

```bash
blueprint-compiler --help
```

---

## Extra

### Extensões

Alguns editores de texto possuem suporte para a linguagem de marcação Blueprint.

Dentro os principais temos:

- [GNU Emacs (DrBluefall)](https://github.com/DrBluefall/blueprint-mode).
- [Visual Studio Code (Bodil Stokke)](https://marketplace.visualstudio.com/items?itemName=bodil.blueprint-gtk).
- [VIM (thetek42)](https://github.com/thetek42/vim-blueprint-syntax).
- [VIM (gabmus)](https://gitlab.com/gabmus/vim-blueprint/-/tree/master).
