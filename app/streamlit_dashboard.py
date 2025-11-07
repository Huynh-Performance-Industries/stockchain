import streamlit as st
from web3 import Web3

INFURA_URL = "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
CONTRACT_ADDRESS = "0xYourContractAddress"
ABI = [
    {"inputs": [], "name": "stockPrice", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}
]

w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

st.title("StockChain Dashboard")
price = contract.functions.stockPrice().call() / 100
st.metric("Current On-Chain Price", f"${price:.2f}")
