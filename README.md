# AgentApi

Kumpulan bot & agent otomatis.

---

## 🤖 Hermes Telegram Agent

Bot Telegram bertenaga AI menggunakan model **Hermes** via **OpenRouter**. Dilengkapi dengan 9 command routes dan router system untuk menangani berbagai jenis permintaan.

### Fitur

- 💬 **Chat Bebas** - Percakapan natural dengan AI Hermes
- 💻 **Code Helper** - Bantuan coding, debugging, dan penjelasan teknis
- 🌐 **Translator** - Terjemahan otomatis antar bahasa
- 📝 **Summarizer** - Ringkasan teks panjang
- ✨ **Creative Writer** - Penulisan kreatif dan imajinatif
- ❓ **Q&A** - Jawab pertanyaan faktual
- 🔄 **Reset** - Reset riwayat percakapan
- 🧠 **Conversation Memory** - Mengingat konteks percakapan
- 🛣️ **9-Route System** - Router modular untuk command handling

### Command Routes

| # | Command | Fungsi |
|---|---------|--------|
| 1 | `/start` | Welcome & pengenalan bot |
| 2 | `/help` | Daftar semua perintah |
| 3 | `/chat <teks>` | Chat bebas dengan AI |
| 4 | `/code <request>` | Bantuan coding |
| 5 | `/translate <teks>` | Terjemahan bahasa |
| 6 | `/summarize <teks>` | Ringkas teks |
| 7 | `/imagine <prompt>` | Penulisan kreatif |
| 8 | `/ask <pertanyaan>` | Tanya fakta |
| 9 | `/reset` | Reset percakapan |

Kirim pesan tanpa command untuk chat bebas langsung!

### Arsitektur

```
hermes_telegram/
├── __init__.py          # Package init
├── config.py            # Konfigurasi dari environment variables
├── agent.py             # Hermes AI agent (OpenRouter API)
├── router.py            # Message router system (9 routes)
├── handlers/
│   ├── __init__.py
│   └── commands.py      # Semua command handlers
└── main.py              # Entry point & bot setup
```

### Instalasi & Setup

```bash
# Clone repo
git clone https://github.com/gondolpancak-boop/AgentApi.git
cd AgentApi

# Install dependencies
pip install -r requirements.txt

# Copy dan isi konfigurasi
cp .env.example .env
# Edit .env dengan token kamu
```

### Konfigurasi

Buat file `.env` dengan isi:

```env
# [WAJIB] Token dari @BotFather di Telegram
TELEGRAM_BOT_TOKEN=your_token_here

# [WAJIB] API Key dari https://openrouter.ai/keys
OPENROUTER_API_KEY=your_key_here

# [OPSIONAL] Model (default: Hermes 3 gratis)
HERMES_MODEL=nousresearch/hermes-3-llama-3.1-405b:free
```

**Cara dapat token:**
1. **Telegram Bot Token**: Chat ke [@BotFather](https://t.me/BotFather) di Telegram → `/newbot` → ikuti instruksi
2. **OpenRouter API Key**: Daftar di [openrouter.ai](https://openrouter.ai) → buat API key di dashboard

### Menjalankan Bot

```bash
# Load env variables dan jalankan
export $(cat .env | xargs)
python run_hermes.py

# Atau langsung set env variables
TELEGRAM_BOT_TOKEN=xxx OPENROUTER_API_KEY=yyy python run_hermes.py
```

### Contoh Penggunaan

```
User: /start
Bot:  👋 Halo! Saya Hermes Agent...

User: /code buatkan fungsi fibonacci di Python
Bot:  def fibonacci(n): ...

User: /translate Good morning, how are you?
Bot:  Selamat pagi, apa kabar? ...

User: /summarize [teks panjang]
Bot:  Ringkasan: ...

User: Halo, siapa kamu?
Bot:  Halo! Saya Hermes, asisten AI kamu...
```

---

## 🔧 Ccode.dev Auto Account Creator Bot

Bot Python untuk membuat akun ccode.dev secara otomatis.

### Fitur

- Email random otomatis
- Auto retry kalau kena rate limit
- Mode interaktif & command line
- Hasil disimpan ke file JSON

### Cara Pakai

```bash
# Mode interaktif
python ccode_bot.py

# Mode command line
python ccode_bot.py -n 10 -a KODE_REFF
```

Lihat `ccode_bot.py` untuk detail lengkap.
