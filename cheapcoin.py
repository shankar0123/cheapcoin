from flask import Flask, jsonify, request
import hashlib
import time

# Define a Block structure
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}".encode()
        return hashlib.sha256(block_string).hexdigest()

# Create the Genesis Block
def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0")

# Store Blockchain
blockchain = [create_genesis_block()]
transactions = []

# Proof-of-Work Function
def proof_of_work(last_proof):
    proof = 0
    while not (proof + last_proof) % 9 == 0:
        proof += 1
    return proof

# Add new blocks with PoW
def create_new_block(previous_block):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    proof = proof_of_work(previous_block.index)
    return Block(index, timestamp, {"transactions": transactions.copy(), "proof-of-work": proof}, previous_hash)

# Flask API
app = Flask(__name__)

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

@app.route('/transaction', methods=['POST'])
def add_transaction():
    tx_data = request.get_json()
    transactions.append(tx_data)
    return jsonify({"message": "Transaction added", "transaction": tx_data}), 201

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

if __name__ == '__main__':
    app.run(port=5000)