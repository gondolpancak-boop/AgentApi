"""Message Router - Routes incoming messages to appropriate handlers."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from telegram import Update
    from telegram.ext import ContextTypes

    HandlerFunc = Callable[
        [Update, ContextTypes.DEFAULT_TYPE],
        Coroutine[Any, Any, None],
    ]


class RouteType(Enum):
    """Types of routes the router can handle."""

    COMMAND = "command"
    TEXT = "text"
    CALLBACK = "callback"


@dataclass
class Route:
    """A single route definition."""

    name: str
    route_type: RouteType
    handler: HandlerFunc
    description: str = ""
    pattern: str | None = None


class MessageRouter:
    """Router that manages 9 command routes + text handler for Hermes bot.

    Routes:
    1. /start    - Welcome & introduction
    2. /help     - Show available commands
    3. /chat     - Free AI conversation
    4. /code     - Code generation & help
    5. /translate - Language translation
    6. /summarize - Text summarization
    7. /imagine  - Creative writing
    8. /ask      - Factual Q&A
    9. /reset    - Reset conversation history

    + Default text handler for free-form chat
    """

    def __init__(self) -> None:
        self._routes: dict[str, Route] = {}
        self._text_handler: HandlerFunc | None = None

    @property
    def routes(self) -> dict[str, Route]:
        """Get all registered routes."""
        return self._routes.copy()

    @property
    def command_routes(self) -> list[Route]:
        """Get only command routes."""
        return [
            r for r in self._routes.values() if r.route_type == RouteType.COMMAND
        ]

    def command(
        self, name: str, description: str = ""
    ) -> Callable[[HandlerFunc], HandlerFunc]:
        """Decorator to register a command route."""

        def decorator(func: HandlerFunc) -> HandlerFunc:
            self._routes[name] = Route(
                name=name,
                route_type=RouteType.COMMAND,
                handler=func,
                description=description,
            )
            return func

        return decorator

    def text_handler(self, func: HandlerFunc) -> HandlerFunc:
        """Decorator to register the default text message handler."""
        self._text_handler = func
        self._routes["_text"] = Route(
            name="_text",
            route_type=RouteType.TEXT,
            handler=func,
            description="Default text message handler",
        )
        return func

    def get_help_text(self) -> str:
        """Generate help text from all registered command routes."""
        lines = ["🤖 *Hermes Agent - Daftar Perintah*\n"]
        for route in self.command_routes:
            if route.description:
                lines.append(f"/{route.name} - {route.description}")
        lines.append("\nAtau kirim pesan langsung untuk chat bebas dengan Hermes!")
        return "\n".join(lines)
