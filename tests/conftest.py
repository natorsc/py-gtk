"""Configurações e fixtures globais para pytest."""

import gi
import pytest

gi.require_version('Gtk', version='4.0')
gi.require_version('Adw', version='1')

from gi.repository import Adw, Gio


@pytest.fixture(scope='session', autouse=True)
def gtk_init():
    """Initialize GTK once per testing session."""
    Adw.init()
    yield


@pytest.fixture
def app():
    """Create a GTK application for testing."""
    application = Adw.Application(
        application_id='br.com.test.App',
        flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
    )
    yield application
    # Cleanup
    application.quit()


@pytest.fixture
def main_loop():
    """Provides access to the GLib MainLoop."""
    from gi.repository import GLib

    loop = GLib.MainLoop()
    yield loop
