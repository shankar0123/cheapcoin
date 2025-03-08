# 🪙 cheapcoin: A Tiny Blockchain & Cryptocurrency in Python  

## 📌 What is cheapcoin?  
cheapcoin is a **minimalistic blockchain implementation** written in **Python** that demonstrates the **fundamentals of how cryptocurrencies work**. It includes:  

✅ A **basic blockchain structure**  
✅ **Proof-of-Work (PoW) mining** ⛏️  
✅ **Transaction handling** 💳  
✅ A **simple Flask API** to interact with the blockchain 🌍  

---

## ⚙️ How cheapcoin Works  

### 🔗 1. The Blockchain Structure  
A **blockchain** is a **linked list of blocks**, where each block contains:  

- **🆔 Index** → Position in the chain  
- **⏳ Timestamp** → When the block was created  
- **📄 Data** → Stores transactions  
- **🔗 Previous Hash** → Reference to the last block (ensuring immutability)  
- **🔒 Block Hash** → Unique identifier (generated using SHA-256)  

Each block’s **hash** is calculated using **SHA-256**:  

```python
def calculate_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()
    return hashlib.sha256(block_string).hexdigest()
```
**🔹 Why is SHA-256 important?**  
✅ Ensures **security** (impossible to reverse-engineer)  
✅ Guarantees **integrity** (modifying a past block invalidates all future blocks)  
✅ Provides **consistency** (fixed-length output)  

---

### 🌱 2. The Genesis Block  
Every blockchain starts with a **Genesis Block** (the first block in the chain).  
Since there is **no previous block**, its **previous hash** is set to `"0"`.  

📌 **Genesis Block Creation:**  
```python
def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0")
```

---

### ⛏️ 3. Proof-of-Work and Mining  
Without a control mechanism, blocks could be **created instantly**, making the blockchain **vulnerable to spam & attacks**.  

**Proof-of-Work (PoW) introduces a computational challenge** that:  
- **Slows down block creation** 🔄  
- **Prevents abuse** 🛑  
- **Ensures security** 🔐  

🔹 **cheapcoin’s PoW Algorithm:**  
- A **miner must find a number (`proof`)** such that:  
  ```bash
  (proof + previous_proof) % 9 == 0
  ```
- **Miners brute-force different numbers** until they find a valid one.  
- The **difficulty** is adjustable by changing the rule.  

📌 **cheapcoin’s PoW Function:**  
```python
def proof_of_work(last_proof):
    proof = 0
    while not (proof + last_proof) % 9 == 0:
        proof += 1
    return proof
```
⏳ **Mining is computationally expensive, securing the blockchain!**  

---

### 🏗️ 4. The Mining Process  
Miners **solve the PoW challenge**, creating a **new block** that is added to the chain. Mining also **rewards miners** by including a **special transaction** in the new block.  

📌 **Mining API in cheapcoin:**  
```python
@app.route('/mine', methods=['GET'])
def mine_block():
    new_block = create_new_block(blockchain[-1])
    blockchain.append(new_block)
    transactions.clear()
    return jsonify({
        "message": "New block mined",
        "block": {
            "index": new_block.index,
            "timestamp": new_block.timestamp,
            "data": new_block.data,
            "previous_hash": new_block.previous_hash,
            "hash": new_block.hash
        }
    })
```
✅ **Mining regulates new coin creation & ensures decentralization**  

---

### 💳 5. Transactions  
Users can **send & receive cheapcoin** via transactions.  
Each transaction contains:  
- **📤 Sender Address**  
- **📥 Receiver Address**  
- **💰 Amount of cheapcoin**  

📌 **Transaction Handling API:**  
```python
transactions = []

@app.route('/transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    transactions.append(tx_data)
    return jsonify({"message": "Transaction added", "transaction": tx_data}), 201
```

📌 **Create a transaction via cURL:**  
```bash
curl -X POST http://127.0.0.1:5000/transaction      -H "Content-Type: application/json"      -d '{"from": "Alice", "to": "Bob", "amount": 10}'
```

🔹 **Transactions remain in memory until a new block is mined.**  

---

### 🌍 6. Viewing the Blockchain  
cheapcoin provides an **API to retrieve the entire blockchain**.  

📌 **Blockchain API:**  
```python
@app.route('/blockchain', methods=['GET'])
def get_blockchain():
    chain_data = [{
        "index": block.index,
        "timestamp": block.timestamp,
        "data": block.data,
        "previous_hash": block.previous_hash,
        "hash": block.hash
    } for block in blockchain]
    return jsonify(chain_data)
```

📌 **Check the blockchain via cURL:**  
```bash
curl http://127.0.0.1:5000/blockchain
```

---

## 🔮 **Next Steps for cheapcoin**  
✅ **Add Wallets & Digital Signatures** 🔐  
✅ **Deploy the Network on Multiple Machines** 🌍  
✅ **Implement a Real Consensus Algorithm** (Replacing longest-chain rule) 🤝  
✅ **Build a Frontend UI** 🎨  