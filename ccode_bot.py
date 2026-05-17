import requests
import json
import time
import re
import random
import string
import argparse

API_URL = "https://ccapi.scydao.com/api/v1/auth/register"
MAX_RETRIES = 3


FIRST_NAMES = [
    "adi", "agus", "ahmad", "andi", "ari", "arif", "bayu", "budi", "cahya",
    "dani", "dedi", "dian", "dwi", "eka", "fajar", "feri", "galih", "gilang",
    "hadi", "hendra", "indra", "irfan", "joko", "kurnia", "luki", "made",
    "nanda", "nova", "okta", "putra", "rafi", "rahmat", "rian", "rizki",
    "sandi", "satria", "surya", "taufik", "wahyu", "yoga", "yusuf", "zainal",
    "anisa", "bella", "citra", "dewi", "eka", "fitri", "gita", "hani",
    "ika", "jeni", "kartika", "lina", "maya", "nita", "putri", "rani",
    "sari", "tika", "wati", "yuli", "zahra", "amel", "bunga", "dinda",
]

LAST_NAMES = [
    "pratama", "saputra", "wijaya", "putra", "kusuma", "nugraha", "hidayat",
    "permana", "santoso", "wibowo", "utama", "lestari", "sari", "rahayu",
    "purnama", "mahendra", "setiawan", "fitriani", "handoko", "susanto",
    "gunawan", "hartono", "suryadi", "firmansyah", "ramadhan", "maulana",
    "hakim", "aditya", "pranata", "laksmana", "anggara", "kurniawan",
]


def generate_random_email(domain="gmail.com"):
    """Generate email dengan nama + angka biar keliatan natural."""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    num = random.randint(1, 9999)
    separator = random.choice(["", ".", "_"])
    return f"{first}{separator}{last}{num}@{domain}"


def create_account(email, password, invitation_code, max_retries=MAX_RETRIES):
    """Buat 1 akun. Otomatis retry kalau kena rate limit."""
    payload = {
        "email": email,
        "password": password,
        "invitation_code": invitation_code
    }
    headers = {"Content-Type": "application/json"}

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.post(API_URL, json=payload, headers=headers, timeout=30)
            data = resp.json()

            if resp.status_code == 200 and data.get("code") == 0:
                user = data["data"]["user"]
                return {
                    "email": email,
                    "password": password,
                    "status": "SUCCESS",
                    "user_id": user["id"],
                    "balance": user["balance"],
                }

            error_msg = data.get("message", str(resp.status_code))

            # Cek rate limit -> otomatis tunggu lalu retry
            wait_match = re.search(r"(\d+)\s*秒", error_msg)
            if wait_match and attempt < max_retries:
                wait_sec = int(wait_match.group(1)) + 2
                print(f"RATE LIMITED, tunggu {wait_sec}s ... ", end="", flush=True)
                time.sleep(wait_sec)
                continue

            return {
                "email": email,
                "password": password,
                "status": "FAILED",
                "error": error_msg,
            }
        except Exception as e:
            if attempt < max_retries:
                print(f"ERROR, retry ({attempt}/{max_retries}) ... ", end="", flush=True)
                time.sleep(3)
                continue
            return {
                "email": email,
                "password": password,
                "status": "ERROR",
                "error": str(e),
            }

    return {"email": email, "password": password, "status": "ERROR", "error": "max retries"}


def interactive_mode():
    """Mode interaktif: tanya user mau bikin berapa akun, kode reff, dll."""
    print()
    print("=" * 60)
    print("  Ccode.dev Auto Account Creator Bot")
    print("  Mode Interaktif")
    print("=" * 60)
    print()

    count = input("Mau bikin berapa akun? [default: 1]: ").strip()
    count = int(count) if count else 1

    aff = input("Kode referral/invitation: ").strip()
    if not aff:
        print("  [!] Kode referral wajib diisi!")
        return

    password = input("Password untuk semua akun [default: 241404]: ").strip()
    password = password if password else "241404"

    delay = input("Delay antar request (detik) [default: 3]: ").strip()
    delay = float(delay) if delay else 3.0

    output = input("Nama file output [default: accounts.json]: ").strip()
    output = output if output else "accounts.json"

    return {
        "count": count,
        "aff": aff,
        "password": password,
        "delay": delay,
        "output": output,
    }


def run_bot(count, aff, password, delay, output):
    """Jalankan bot untuk bikin akun."""
    print()
    print("=" * 60)
    print("  Ccode.dev Auto Account Creator Bot")
    print("=" * 60)
    print(f"  Jumlah akun  : {count}")
    print(f"  Password     : {password}")
    print(f"  Referral     : {aff}")
    print(f"  Delay        : {delay}s")
    print(f"  Output       : {output}")
    print("=" * 60)
    print()

    results = []
    success = 0
    failed = 0

    for i in range(1, count + 1):
        email = generate_random_email()
        print(f"[{i}/{count}] Creating: {email} ... ", end="", flush=True)
        result = create_account(email, password, aff)
        results.append(result)

        if result["status"] == "SUCCESS":
            success += 1
            print(f"SUCCESS (ID: {result['user_id']}, Balance: ${result['balance']})")
        else:
            failed += 1
            print(f"FAILED ({result.get('error', 'unknown')})")

        if i < count:
            time.sleep(delay)

    # Save results
    with open(output, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print()
    print("=" * 60)
    print("  HASIL")
    print("=" * 60)
    print(f"  Total    : {count}")
    print(f"  Sukses   : {success}")
    print(f"  Gagal    : {failed}")
    print(f"  Output   : {output}")
    print("=" * 60)

    print()
    print("Daftar Akun:")
    print("-" * 60)
    for r in results:
        status_icon = "OK" if r["status"] == "SUCCESS" else "XX"
        print(f"  [{status_icon}] {r['email']} / {r['password']}")
    print("-" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Ccode.dev Auto Account Creator Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  # Mode interaktif (ditanya satu per satu)
  python ccode_bot.py

  # Langsung bikin 10 akun
  python ccode_bot.py -n 10 -a KODE_REFF

  # Bikin 5 akun dengan password custom
  python ccode_bot.py -n 5 -a KODE_REFF -p mypassword123

  # Bikin 20 akun dengan delay 5 detik
  python ccode_bot.py -n 20 -a KODE_REFF -d 5
        """
    )
    parser.add_argument("-n", "--count", type=int, help="Jumlah akun yang mau dibuat")
    parser.add_argument("-p", "--password", type=str, default="241404", help="Password untuk semua akun (default: 241404)")
    parser.add_argument("-a", "--aff", type=str, help="Kode referral/invitation (WAJIB)")
    parser.add_argument("-d", "--delay", type=float, default=3.0, help="Delay antar request dalam detik (default: 3)")
    parser.add_argument("-o", "--output", type=str, default="accounts.json", help="File output hasil (default: accounts.json)")

    args = parser.parse_args()

    # Kalau tidak ada argumen -n dan -a, masuk mode interaktif
    if args.count is None or args.aff is None:
        config = interactive_mode()
        if config is None:
            return
        run_bot(**config)
    else:
        run_bot(
            count=args.count,
            aff=args.aff,
            password=args.password,
            delay=args.delay,
            output=args.output,
        )


if __name__ == "__main__":
    main()
