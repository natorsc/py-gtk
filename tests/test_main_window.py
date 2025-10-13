"""Testes para janelas."""

import pytest
from MainWindow import ExampleWindow


@pytest.mark.unit
def test_window_creation(app):
    window = ExampleWindow(application=app)
    assert window is not None
    assert window.get_title() == 'Python - PyGObject - GTK'


@pytest.mark.unit
def test_window_size(app):
    window = ExampleWindow(application=app)
    assert window.get_default_size() == (683, 384)


@pytest.mark.gui
def test_window_widgets(app):
    """Tests if widgets were created (self.widget)."""
    window = ExampleWindow(application=app)
    assert hasattr(window, 'adw_status_page')
