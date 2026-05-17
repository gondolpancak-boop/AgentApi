# Ccode.dev Auto Account Creator Bot

Bot Python untuk membuat akun ccode.dev secara otomatis.

## Fitur

- Email random otomatis (tidak perlu punya Gmail asli)
- Auto retry kalau kena rate limit
- Mode interaktif (ditanya satu per satu)
- Mode command line (langsung jalankan dengan parameter)
- Hasil disimpan ke file JSON
- Bisa atur jumlah akun, password, kode referral, delay

## Instalasi

```bash
# Clone repo
git clone https://github.com/gondolpancak-boop/ccode-bot.git
cd ccode-bot

# Install dependency
pip install requests
```

## Cara Pakai

### Mode Interaktif

Tinggal jalankan tanpa parameter, nanti ditanya satu per satu:

```bash
python ccode_bot.py
```

Output:
```
============================================================
  Ccode.dev Auto Account Creator Bot
  Mode Interaktif
============================================================

Mau bikin berapa akun? [default: 1]: 5
Kode referral/invitation: KODE_REFF_KAMU
Password untuk semua akun [default: 241404]: 
Delay antar request (detik) [default: 3]: 
Nama file output [default: accounts.json]: 
```

### Mode Command Line

Langsung bikin akun tanpa ditanya:

```bash
# Bikin 10 akun
python ccode_bot.py -n 10 -a KODE_REFF_KAMU

# Bikin 5 akun dengan password custom
python ccode_bot.py -n 5 -a KODE_REFF_KAMU -p mypassword123

# Bikin 20 akun dengan delay 5 detik
python ccode_bot.py -n 20 -a KODE_REFF_KAMU -d 5

# Bikin 10 akun dan simpan ke file custom
python ccode_bot.py -n 10 -a KODE_REFF_KAMU -o hasil.json
```

### Parameter

| Parameter | Keterangan | Default |
|-----------|------------|---------|
| `-n` / `--count` | Jumlah akun yang mau dibuat | (wajib di CLI mode) |
| `-a` / `--aff` | Kode referral/invitation | (wajib) |
| `-p` / `--password` | Password untuk semua akun | `241404` |
| `-d` / `--delay` | Delay antar request (detik) | `3` |
| `-o` / `--output` | File output hasil | `accounts.json` |

## Output

Hasil pembuatan akun disimpan ke file `accounts.json`:

```json
[
  {
    "email": "abc123xyz@gmail.com",
    "password": "241404",
    "status": "SUCCESS",
    "user_id": 12345,
    "balance": 1
  }
]
```

## Tips

- Kalau kena rate limit, bot otomatis tunggu lalu retry (max 3x)
- Disarankan pakai delay minimal 3 detik supaya tidak sering kena rate limit
- Kalau mau bikin banyak akun (50+), pakai delay 5 detik biar aman
