import requests, time, os
from web3 import Web3

STOCK_SYMBOL = "AAPL"
API_KEY = os.getenv("ALPHA_VANTAGE_KEY")
CONTRACT_ADDRESS = "0xYourDeployedContractAddress"
ORACLE_PRIVATE_KEY = os.getenv("PRIVATE_KEY")
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"

ABI = [
    {
        "inputs": [{"internalType": "uint256", "name": "_newPrice", "type": "uint256"}],
        "name": "updatePrice",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
account = w3.eth.account.from_key(ORACLE_PRIVATE_KEY)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def get_stock_price(symbol):
    r = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}").json()
    return int(float(r["Global Quote"]["05. price"]) * 100)

def update_contract_price(new_price):
    n = w3.eth.get_transaction_count(account.address)
    txn = contract.functions.updatePrice(new_price).build_transaction({
        "from": account.address,
        "nonce": n,
        "gas": 200000,
        "gasPrice": w3.to_wei("15", "gwei")
    })
    signed = w3.eth.account.sign_transaction(txn, ORACLE_PRIVATE_KEY)
    tx = w3.eth.send_raw_transaction(signed.rawTransaction)
    print(f"Updated price: ${new_price/100:.2f} | Tx: {tx.hex()}")

if __name__ == "__main__":
    while True:
        try:
            price = get_stock_price(STOCK_SYMBOL)
            update_contract_price(price)
        except Exception as e:
            print(e)
        time.sleep(300)
