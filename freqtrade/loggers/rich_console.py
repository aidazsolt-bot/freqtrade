import sys
from shutil import get_terminal_size

from rich.console import Console


def console_width() -> int | None:
    """
    Get the width of the console
    """
    if any(module in ["pytest", "ipykernel"] for module in sys.modules):
        return 200

    width, _ = get_terminal_size((1, 24))
    # Fall back to 200 if terminal size is not available.
    # This is determined by assuming an insane width of 1char, which is unlikely.
    w = None if width > 1 else 200
    return w


def get_rich_console(**kwargs) -> Console:
    """
    Get a rich console with default settings

    Rich 15+ treats dumb/non-TTY terminals as 80 columns unless both width and
    height are set; width-only is ignored. Always pair an explicit width with a
    height so pytest and redirected output keep a usable table width.
    """
    width = kwargs.get("width", console_width())
    kwargs["width"] = width
    if width is not None:
        kwargs.setdefault("height", 25)
    return Console(**kwargs)
