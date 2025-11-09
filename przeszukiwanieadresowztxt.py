import requests
import time
import random
import os

PLIK_WEJSCIOWY = "bitcoinznalezione.txt"
PLIK_WYJSCIOWY = "adresyzsaldem.txt"
PLIK_OSTATNI_ADRES = "ostatni_adres.txt"  # Plik do przechowywania ostatniego przetwarzanego adresu

API_LIST = [
    "https://api.blockcypher.com/v1/btc/main/addrs/{}/balance",  # BlockCypher
    "https://blockchain.info/q/addressbalance/{}",  # Blockchain.info
    "https://api.blockstream.info/api/address/{}/txs",  # BlockStream
    "https://btcscan.org/api/address/{}/balance",  # BTCScan
    "https://api.blockchair.com/bitcoin/dashboards/address/{}",  # BlockChair
    "https://chain.api.btc.com/v3/address/{}/balance",  # BTC.com
    "https://mempool.space/api/address/{}",  # Mempool
    "https://sochain.com/api/v2/address/BTC/{}",  # SoChain
    "https://blockchain.info/rawaddr/{}",  # Blockchain.info raw
    "https://blockcypher.com/api/v1/btc/main/addresses/{}/balance"  # BlockCypher alternate
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

# Funkcja do pobierania salda
def sprawdz_saldo(adres):
    random.shuffle(API_LIST)  # Shuffle the API list to avoid getting blocked
    for api in API_LIST:
        url = api.format(adres)
        try:
            response = requests.get(url, headers=get_headers(), timeout=15)
            if response.status_code == 200:
                try:
                    # Bezpieczne parsowanie odpowiedzi JSON
                    data = response.json()
                    if isinstance(data, dict):  # Sprawdzamy, czy data jest słownikiem
                        if 'balance' in data:
                            return int(data['balance'])
                        elif 'final_balance' in data:
                            return int(data['final_balance'])
                        else:
                            print(f"⚠️ Nieoczekiwany format odpowiedzi z API: {url}")
                            continue  # Przechodzimy do następnego API
                    else:
                        print(f"❌ Otrzymano nieoczekiwaną odpowiedź: {data}")
                        continue  # Przechodzimy do następnego API
                except ValueError:
                    print(f"❌ Błąd parsowania JSON z API: {url}")
                    continue  # Przechodzimy do następnego API
            elif response.status_code in [403, 429]:
                print(f"⚠️ API {url} zablokowało nas – przechodzimy do innego.")
                continue  # Przechodzimy do następnego API
        except requests.exceptions.RequestException:
            print(f"❌ Błąd przy połączeniu z API: {url}")
            continue  # Przechodzimy do następnego API
        time.sleep(random.uniform(10, 30))  # Random sleep to avoid flooding the server
    return 0  # Jeśli wszystkie API zawiodą, zwróć 0

# Funkcja zapisująca adres do pliku
def zapisz_adres(adres):
    saldo = sprawdz_saldo(adres)
    if saldo > 0:
        with open(PLIK_WYJSCIOWY, "a", encoding="utf-8") as plik:
            plik.write(adres + "\n")
        print(f"✅ Adres {adres} ma saldo: {saldo} satoshi")
    else:
        print(f"❌ Adres {adres} nie ma salda.")

# Funkcja zapisz ostatni przetworzony adres
def zapisz_ostatni_adres(adres):
    with open(PLIK_OSTATNI_ADRES, "w", encoding="utf-8") as plik:
        plik.write(adres)
    print(f"📝 Zapisano ostatni przetworzony adres: {adres}")

# Funkcja wczytująca ostatni przetworzony adres
def wczytaj_ostatni_adres():
    if os.path.exists(PLIK_OSTATNI_ADRES):
        with open(PLIK_OSTATNI_ADRES, "r", encoding="utf-8") as plik:
            return plik.read().strip()
    return None

# Funkcja przetwarzająca plik wejściowy
def przetworz_adresy():
    # Wczytanie wszystkich adresów z pliku wejściowego
    with open(PLIK_WEJSCIOWY, "r", encoding="utf-8") as plik:
        adresy = [linia.split('Bitcoin Address:')[1].strip() for linia in plik.readlines() if "Bitcoin Address" in linia]
    
    # Wczytanie ostatniego przetworzonego adresu, jeśli istnieje
    ostatni_adres = wczytaj_ostatni_adres()

    # Znajdowanie indeksu ostatniego adresu w liście i rozpoczynanie od następnego
    if ostatni_adres:
        if ostatni_adres in adresy:
            adresy = adresy[adresy.index(ostatni_adres) + 1:]
        else:
            print(f"⚠️ Ostatni adres {ostatni_adres} nie został znaleziony w pliku, rozpoczynamy od początku.")
    
    # Przetwarzanie adresów
    for adres in adresy:
        try:
            zapisz_adres(adres)
            zapisz_ostatni_adres(adres)  # Zapisz ostatni przetworzony adres
            time.sleep(random.uniform(30, 60))  # Opóźnienie między zapytaniami
        except Exception as e:
            print(f"❌ Błąd podczas przetwarzania adresu {adres}: {e}")
            continue  # Przechodzimy do następnego adresu

# Uruchomienie skryptu
przetworz_adresy()
print("✅ Proces zakończony.")
