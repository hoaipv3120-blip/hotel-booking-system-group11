import pytest
from src.main import main_menu

def test_main_menu_input(monkeypatch):
    # Giả lập nhập "1"
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert main_menu() == "1"
