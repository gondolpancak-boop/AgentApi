"""Hermes Telegram Agent - Main entry point."""

import logging
import sys

from .agent import HermesAgent
from .config import Config
from .handlers import register_all_handlers

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Start the Hermes Telegram bot."""
    from telegram.ext import Application

    config = Config.from_env()
    errors = config.validate()
    if errors:
        for err in errors:
            logger.error("Config error: %s", err)
        logger.error(
            "Set environment variables TELEGRAM_BOT_TOKEN and OPENROUTER_API_KEY"
        )
        sys.exit(1)

    agent = HermesAgent(config)

    app = Application.builder().token(config.telegram_token).build()

    app.bot_data["agent"] = agent
    app.bot_data["config"] = config

    registered_router = register_all_handlers(app)

    command_count = len(registered_router.command_routes)
    logger.info(
        "Hermes Agent started with %d command routes", command_count
    )
    for route in registered_router.command_routes:
        logger.info("  /%s - %s", route.name, route.description)

    logger.info("Bot is running... Press Ctrl+C to stop.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
