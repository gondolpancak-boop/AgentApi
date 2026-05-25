"""Hermes AI Agent - Core LLM interaction layer."""

import httpx

from .config import Config


class HermesAgent:
    """AI agent powered by Hermes model via OpenRouter."""

    def __init__(self, config: Config) -> None:
        self.config = config
        self._conversations: dict[int, list[dict[str, str]]] = {}

    def get_history(self, chat_id: int) -> list[dict[str, str]]:
        """Get conversation history for a chat."""
        if chat_id not in self._conversations:
            self._conversations[chat_id] = []
        return self._conversations[chat_id]

    def clear_history(self, chat_id: int) -> None:
        """Clear conversation history for a chat."""
        self._conversations.pop(chat_id, None)

    def _build_messages(
        self,
        chat_id: int,
        user_message: str,
        system_override: str | None = None,
    ) -> list[dict[str, str]]:
        """Build the messages array for the API call."""
        system_prompt = system_override or self.config.system_prompt
        history = self.get_history(chat_id)

        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    async def chat(
        self,
        chat_id: int,
        user_message: str,
        system_override: str | None = None,
    ) -> str:
        """Send a message to Hermes and get a response."""
        messages = self._build_messages(chat_id, user_message, system_override)

        payload = {
            "model": self.config.hermes_model,
            "messages": messages,
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.config.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/gondolpancak-boop/AgentApi",
            "X-Title": "Hermes Telegram Agent",
        }

        try:
            async with httpx.AsyncClient(timeout=60) as client:
                response = await client.post(
                    f"{self.config.openrouter_base_url}/chat/completions",
                    json=payload,
                    headers=headers,
                )
                response.raise_for_status()
                data = response.json()

            reply = data["choices"][0]["message"]["content"]

            history = self.get_history(chat_id)
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": reply})

            if len(history) > self.config.max_history * 2:
                self._conversations[chat_id] = history[
                    -(self.config.max_history * 2) :
                ]

            return reply

        except httpx.HTTPStatusError as e:
            return f"❌ API Error: {e.response.status_code} - {e.response.text[:200]}"
        except httpx.RequestError as e:
            return f"❌ Connection Error: {e}"
        except (KeyError, IndexError):
            return "❌ Unexpected response from AI model."
