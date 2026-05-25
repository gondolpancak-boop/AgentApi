"""Configuration management for Hermes Telegram Agent."""

import os
from dataclasses import dataclass, field


@dataclass
class Config:
    """Bot configuration loaded from environment variables."""

    telegram_token: str = ""
    openrouter_api_key: str = ""
    hermes_model: str = "nousresearch/hermes-3-llama-3.1-405b:free"
    openrouter_base_url: str = "https://openrouter.ai/api/v1"
    max_history: int = 20
    max_tokens: int = 2048
    temperature: float = 0.7
    system_prompt: str = (
        "Kamu adalah Hermes, asisten AI yang cerdas dan ramah. "
        "Kamu bisa membantu dengan berbagai tugas termasuk coding, "
        "terjemahan, ringkasan, dan percakapan umum. "
        "Jawab dengan bahasa yang sama dengan user."
    )
    command_prompts: dict = field(default_factory=lambda: {
        "chat": "Kamu adalah asisten AI yang ramah. Jawab pertanyaan user dengan jelas.",
        "code": (
            "Kamu adalah programmer expert. Bantu user dengan kode, debugging, "
            "dan penjelasan teknis. Selalu berikan contoh kode yang bisa dijalankan."
        ),
        "translate": (
            "Kamu adalah penerjemah profesional. Terjemahkan teks yang diberikan. "
            "Jika teks dalam bahasa Indonesia, terjemahkan ke bahasa Inggris. "
            "Jika teks dalam bahasa lain, terjemahkan ke bahasa Indonesia. "
            "Berikan juga penjelasan singkat tentang konteks terjemahan."
        ),
        "summarize": (
            "Kamu adalah ahli meringkas teks. Buat ringkasan yang padat dan informatif "
            "dari teks yang diberikan. Gunakan bullet points jika perlu."
        ),
        "imagine": (
            "Kamu adalah penulis kreatif. Buat tulisan kreatif, cerita, puisi, "
            "atau deskripsi imajinatif berdasarkan prompt yang diberikan."
        ),
        "ask": (
            "Kamu adalah ensiklopedia berjalan. Jawab pertanyaan faktual "
            "dengan akurat dan detail. Sertakan sumber jika memungkinkan."
        ),
    })

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        return cls(
            telegram_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY", ""),
            hermes_model=os.getenv(
                "HERMES_MODEL", "nousresearch/hermes-3-llama-3.1-405b:free"
            ),
            openrouter_base_url=os.getenv(
                "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"
            ),
            max_history=int(os.getenv("MAX_HISTORY", "20")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2048")),
            temperature=float(os.getenv("TEMPERATURE", "0.7")),
        )

    def validate(self) -> list[str]:
        """Validate required configuration. Returns list of errors."""
        errors = []
        if not self.telegram_token:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        if not self.openrouter_api_key:
            errors.append("OPENROUTER_API_KEY is required")
        return errors
