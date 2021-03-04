from datetime import datetime
from typing import Iterable, List, Optional, TYPE_CHECKING, Union, Callable


from .text import Text, TextType

if TYPE_CHECKING:
    from .console import Console, ConsoleRenderable, RenderableType
    from .table import Table

FormatTimeCallable = Callable[[datetime], Text]


class LogRender:
    def __init__(
        self,
        show_time: bool = True,
        show_level: bool = False,
        show_path: bool = True,
        time_format: Union[str, FormatTimeCallable] = "[%x %X]",
        level_width: Optional[int] = 8,
    ) -> None:
        self.show_time = show_time
        self.show_level = show_level
        self.show_path = show_path
        self.time_format = time_format
        self.level_width = level_width
        self._last_time: Optional[Text] = None

    def __call__(
        self,
        console: "Console",
        renderables: Iterable["ConsoleRenderable"],
        log_time: datetime = None,
        time_format: Union[str, FormatTimeCallable] = None,
        level: TextType = "",
        path: str = None,
        line_no: int = None,
        link_path: str = None,
    ) -> "Table":
        from .containers import Renderables
        from .table import Table

        output = Table.grid(padding=(0, 1))
        output.expand = True
        if self.show_time:
            output.add_column(style="log.time")
        if self.show_level:
            output.add_column(style="log.level", width=self.level_width)
        output.add_column(ratio=1, style="log.message", overflow="fold")
        if self.show_path and path:
            output.add_column(style="log.path")
        row: List["RenderableType"] = []
        if self.show_time:
            log_time = log_time or console.get_datetime()
            time_format = time_format or self.time_format
            if callable(time_format):
                log_time_display = time_format(log_time)
            else:
                log_time_display = Text(log_time.strftime(time_format))
            if log_time_display == self._last_time:
                row.append(Text(" " * len(log_time_display)))
            else:
                row.append(log_time_display)
                self._last_time = log_time_display
        if self.show_level:
            row.append(level)

        row.append(Renderables(renderables))
        if self.show_path and path:
            path_text = Text()
            path_text.append(
                path, style=f"link file://{link_path}" if link_path else ""
            )
            if line_no:
                path_text.append(f":{line_no}")
            row.append(path_text)

        output.add_row(*row)
        return output


if __name__ == "__main__":  # pragma: no cover
    from rich.console import Console

    c = Console()
    c.print("[on blue]Hello", justify="right")
    c.log("[on blue]hello", justify="right")
