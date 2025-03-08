cheapcoin: A Tiny Blockchain & Cryptocurrency in Python

What is cheapcoin?

cheapcoin is a minimalistic blockchain implementation written in Python that demonstrates the fundamentals of how cryptocurrencies work. It includes:
	•	A basic blockchain structure
	•	Proof-of-Work (PoW) mining
	•	Transaction handling
	•	A simple Flask API to interact with the blockchain

⸻

How cheapcoin Works

1. The Blockchain Structure

A blockchain is essentially a linked list of blocks, where each block contains:
	•	Index – Position in the chain
	•	Timestamp – When the block was created
	•	Data – Stores transactions
	•	Previous Hash – A reference to the last block, ensuring immutability
	•	Block Hash – A unique identifier for the block, generated using SHA-256

Each block’s hash is calculated using this function:

def calculate_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()
    return hashlib.sha256(block_string).hexdigest()

This ensures that every block is cryptographically linked to the previous one. Any attempt to modify past data would invalidate all subsequent blocks, making tampering nearly impossible.

⸻

2. The Genesis Block

Every blockchain starts with a genesis block, the first block in the chain. Since there is no previous block, its previous hash is set to "0".

def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0")



⸻

3. Proof-of-Work and Mining

Without a control mechanism, new blocks could be created instantly, making the blockchain vulnerable to spam and attacks. Proof-of-Work (PoW) introduces a computational challenge to slow down block creation and secure the network.

cheapcoin’s PoW algorithm is simple:
	•	A miner must find a number (proof) such that:

(proof + previous_proof) % 9 == 0


	•	Miners try different numbers until they find a valid one.
	•	The difficulty is adjustable by changing the rule.

This is the function that miners use to find a valid proof:

def proof_of_work(last_proof):
    proof = 0
    while not (proof + last_proof) % 9 == 0:
        proof += 1
    return proof

By making mining computationally expensive, PoW ensures that adding blocks requires real effort, preventing easy manipulation of the blockchain.

⸻

4. The Mining Process

When a miner solves the PoW challenge, a new block is created and added to the chain. Mining also rewards the miner by including a special transaction in the new block.

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

Mining regulates the creation of new coins and ensures the blockchain remains secure and decentralized.

⸻

5. Transactions

Transactions allow users to send and receive cheapcoin. Each transaction contains:
	•	The sender’s address
	•	The receiver’s address
	•	The amount transferred

Transactions are added to a list and stored in the next block that gets mined.

transactions = []

@app.route('/transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    transactions.append(tx_data)
    return jsonify({"message": "Transaction added", "transaction": tx_data}), 201

To add a transaction:

curl -X POST http://127.0.0.1:5000/transaction \
     -H "Content-Type: application/json" \
     -d '{"from": "Alice", "to": "Bob", "amount": 10}'

Transactions remain in memory until they are included in a block.

⸻

6. Viewing the Blockchain

cheapcoin provides an API to retrieve the entire blockchain.

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

To check the blockchain:

curl http://127.0.0.1:5000/blockchain

This returns the full history of blocks, showing transactions and proof-of-work solutions.

⸻

The Flow of cheapcoin
	1.	The blockchain starts with a genesis block.
	2.	Users create transactions.
	3.	Miners collect transactions and mine a new block.
	4.	Proof-of-Work ensures that mining is computationally expensive.
	5.	The new block is verified and added to the blockchain.
	6.	The miner is rewarded with newly created cheapcoin.
	7.	Users can check the blockchain to verify all transactions.

⸻

Running cheapcoin Locally

1. Create a Virtual Environment

uv venv .venv
source .venv/bin/activate

2. Install Dependencies

uv pip install flask

3. Start the Blockchain API

python3 cheapcoin.py

4. Test Transactions

curl -X POST http://127.0.0.1:5000/transaction \
     -H "Content-Type: application/json" \
     -d '{"from": "Alice", "to": "Bob", "amount": 10}'

5. Mine a Block

curl http://127.0.0.1:5000/mine

6. View the Blockchain

curl http://127.0.0.1:5000/blockchain

⸻

Next Steps

	•	Wallets and digital signatures for secure transactions
	•	A peer-to-peer network to support decentralization
	•	A real consensus algorithm to replace simple longest-chain verification
	•	A front-end interface for users to interact with the blockchain
