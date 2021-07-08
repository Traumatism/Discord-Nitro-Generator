from os import stat
from rich.console import Console

class Logging:
    console = Console()

    @staticmethod
    def print(
        content: str,
        prefix: str,
        prefix_color: str
    ) -> None:
        Logging.console.print(
            f'[{prefix_color}][{prefix}][/{prefix_color}] {content}'
        )

    @staticmethod
    def success(content: str) -> None:
        Logging.print(
            content=content,
            prefix='+',
            prefix_color='bright_green'
        )

    @staticmethod
    def info(content: str) -> None:
        Logging.print(
            content=content,
            prefix='*',
            prefix_color='bright_blue'
        )

    @staticmethod
    def error(content: str) -> None:
        Logging.print(
            content=content,
            prefix='-',
            prefix_color='bright_yellow'
        )