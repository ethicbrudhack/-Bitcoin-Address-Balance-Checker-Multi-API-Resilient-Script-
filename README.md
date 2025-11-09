# 💰 Bitcoin Address Balance Checker (Multi-API Resilient Script)

This Python script automatically checks the **balances of multiple Bitcoin addresses** using several public blockchain APIs (BlockCypher, Blockchain.info, Blockstream, Mempool, etc.).  
It reads a list of addresses from an input file, queries multiple APIs for each address, saves those with a non-zero balance to a separate file, and remembers the last processed address to resume safely after interruptions.

---

## 🧩 Overview

This tool is designed for researchers, developers, and auditors who need to:
- Check which Bitcoin addresses (from a list) still hold funds.
- Automate API queries without getting blocked.
- Resume scanning from where it stopped after a crash or connection loss.

It performs load-balanced queries across **multiple blockchain APIs** and introduces random time delays and user agents to reduce the risk of temporary bans or rate limits.

---

## ⚙️ How It Works

1. **Input File** (`bitcoinznalezione.txt`)  
   Contains Bitcoin addresses to be checked.  
   Example format:
itcoin Address: bc1qexampleaddress1
Bitcoin Address: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa


2. **For each address**, the script:
- Randomly selects an API endpoint from a predefined list.
- Sends an HTTP GET request to fetch balance information.
- Parses the JSON response and extracts the balance (in satoshis).
- If the balance > 0 → saves the address to `adresyzsaldem.txt`.

3. **Resilience & Recovery:**
- Keeps track of the **last successfully processed address** in `ostatni_adres.txt`.
- Automatically resumes scanning from that point on restart.
- Waits randomly between 30–60 seconds between requests to avoid API throttling.

4. **APIs Used:**
- BlockCypher  
- Blockchain.info  
- Blockstream.info  
- BTCScan  
- BlockChair  
- BTC.com  
- Mempool.space  
- SoChain  
(shuffled randomly for each query)

---

## 🧮 File Structure

| File | Purpose |
|------|----------|
| `bitcoinznalezione.txt` | Input file containing addresses to check |
| `adresyzsaldem.txt` | Output file where addresses with non-zero balance are saved |
| `ostatni_adres.txt` | Stores the last processed address to allow continuation |

---

## 🧾 Example Output



✅ Address bc1qexample1 has balance: 123456 satoshi
❌ Address bc1qexample2 has no balance.
📝 Saved last processed address: bc1qexample2
✅ Process completed.


---

## 🚀 Usage

1. **Prepare your input file** (`bitcoinznalezione.txt`)  
   Add one or more lines like:


Bitcoin Address: bc1qexampleaddress


2. **Install dependencies:**
```bash
pip install requests


Run the script:

python3 check_bitcoin_balances.py


Monitor output:

Found addresses with balance → written to adresyzsaldem.txt

Progress checkpoint → stored in ostatni_adres.txt

🧠 Key Features

✅ Queries multiple APIs to improve reliability
✅ Handles network errors and API bans automatically
✅ Randomizes user agents and delays for safer scraping
✅ Resumable scan (auto-continue from last address)
✅ Zero external dependencies beyond requests

⚠️ Security & Ethics Notice

⚠️ For legitimate research and monitoring only.
Do not use this script for unauthorized scanning of wallets or addresses that are not yours.
Public APIs may rate-limit or block excessive requests.
Always respect API usage policies.
Handle data responsibly — especially if scanning real wallets.

BTC donation address: bc1q4nyq7kr4nwq6zw35pg0zl0k9jmdmtmadlfvqhr
