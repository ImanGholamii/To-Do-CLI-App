from todo_cli_app.utils import timeit_print, confirm


def test_timeit_print_decorator(capsys):
    @timeit_print
    def small(a, b):
        return a + b

    result = small(2, 3)
    captured = capsys.readouterr()
    assert result == 5
    # timeit prints something like "[timeit] small took 0.00xxs"
    assert "[timeit]" in captured.out


def test_confirm_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "y")
    assert confirm("anything?") is True


def test_confirm_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt="": "n")
    assert confirm("anything?") is False
