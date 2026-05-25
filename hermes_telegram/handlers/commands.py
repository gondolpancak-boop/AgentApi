"""All command handlers for the Hermes Telegram bot."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ..agent import HermesAgent
from ..config import Config
from ..router import MessageRouter

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes

router = MessageRouter()


def _get_text_after_command(text: str | None) -> str:
    """Extract text after a /command."""
    if not text:
        return ""
    parts = text.split(maxsplit=1)
    return parts[1] if len(parts) > 1 else ""


# ─── Route 1: /start ───────────────────────────────────────────────────────────

@router.command("start", description="Mulai bot & lihat intro")
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome message when user starts the bot."""
    welcome = (
        "👋 *Halo! Saya Hermes Agent*\n\n"
        "Saya asisten AI yang siap membantu kamu dengan:\n"
        "• 💬 Chat & percakapan\n"
        "• 💻 Bantuan coding\n"
        "• 🌐 Terjemahan bahasa\n"
        "• 📝 Ringkasan teks\n"
        "• ✨ Penulisan kreatif\n"
        "• ❓ Menjawab pertanyaan\n\n"
        "Ketik /help untuk melihat semua perintah,\n"
        "atau langsung kirim pesan untuk mulai chat!"
    )
    if update.message:
        await update.message.reply_text(welcome, parse_mode="Markdown")


# ─── Route 2: /help ────────────────────────────────────────────────────────────

@router.command("help", description="Tampilkan daftar perintah")
async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show all available commands."""
    if update.message:
        await update.message.reply_text(
            router.get_help_text(), parse_mode="Markdown"
        )


# ─── Route 3: /chat ────────────────────────────────────────────────────────────

@router.command("chat", description="Chat bebas dengan Hermes AI")
async def cmd_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Free-form AI conversation."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "💬 Kirim pesan setelah /chat\n"
            "Contoh: `/chat apa kabar hari ini?`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["chat"]
    )
    await update.message.reply_text(reply)


# ─── Route 4: /code ────────────────────────────────────────────────────────────

@router.command("code", description="Bantuan coding & programming")
async def cmd_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Code generation and programming help."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "💻 Kirim request coding setelah /code\n"
            "Contoh: `/code buatkan fungsi Python untuk sorting`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["code"]
    )
    await update.message.reply_text(reply)


# ─── Route 5: /translate ───────────────────────────────────────────────────────

@router.command("translate", description="Terjemahkan teks")
async def cmd_translate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Translate text between languages."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "🌐 Kirim teks setelah /translate\n"
            "Contoh: `/translate Hello, how are you?`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["translate"]
    )
    await update.message.reply_text(reply)


# ─── Route 6: /summarize ───────────────────────────────────────────────────────

@router.command("summarize", description="Ringkas teks panjang")
async def cmd_summarize(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarize long text."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "📝 Kirim teks panjang setelah /summarize\n"
            "Contoh: `/summarize [teks panjang di sini]`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["summarize"]
    )
    await update.message.reply_text(reply)


# ─── Route 7: /imagine ─────────────────────────────────────────────────────────

@router.command("imagine", description="Penulisan kreatif & imajinatif")
async def cmd_imagine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Creative writing and imaginative content."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "✨ Kirim prompt kreatif setelah /imagine\n"
            "Contoh: `/imagine ceritakan tentang robot di masa depan`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["imagine"]
    )
    await update.message.reply_text(reply)


# ─── Route 8: /ask ─────────────────────────────────────────────────────────────

@router.command("ask", description="Tanya fakta & pengetahuan")
async def cmd_ask(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Factual question answering."""
    if not update.message:
        return

    text = _get_text_after_command(update.message.text)
    if not text:
        await update.message.reply_text(
            "❓ Kirim pertanyaan setelah /ask\n"
            "Contoh: `/ask siapa penemu lampu pijar?`",
            parse_mode="Markdown",
        )
        return

    agent: HermesAgent = context.bot_data["agent"]
    config: Config = context.bot_data["config"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(
        update.message.chat_id, text, config.command_prompts["ask"]
    )
    await update.message.reply_text(reply)


# ─── Route 9: /reset ───────────────────────────────────────────────────────────

@router.command("reset", description="Reset riwayat percakapan")
async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reset conversation history."""
    if not update.message:
        return

    agent: HermesAgent = context.bot_data["agent"]
    agent.clear_history(update.message.chat_id)
    await update.message.reply_text(
        "🔄 Riwayat percakapan telah direset!\n"
        "Kirim pesan baru untuk memulai percakapan baru."
    )


# ─── Default Text Handler ──────────────────────────────────────────────────────

@router.text_handler
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle free-form text messages (no command prefix)."""
    if not update.message or not update.message.text:
        return

    agent: HermesAgent = context.bot_data["agent"]
    await update.message.chat.send_action("typing")
    reply = await agent.chat(update.message.chat_id, update.message.text)
    await update.message.reply_text(reply)


def register_all_handlers(app: "object") -> MessageRouter:
    """Register all handlers with the Telegram application.

    Returns the router instance for reference.
    """
    from telegram.ext import CommandHandler, MessageHandler, filters

    for route in router.command_routes:
        app.add_handler(CommandHandler(route.name, route.handler))  # type: ignore[attr-defined]

    if router._text_handler:
        app.add_handler(  # type: ignore[attr-defined]
            MessageHandler(
                filters.TEXT & ~filters.COMMAND, router._text_handler
            )
        )

    return router
