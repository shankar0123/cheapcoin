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

# Create the Genesis Block (first block)
def create_genesis_block():
    return Block(0, time.time(), "Genesis Block", "0")

# Test it
genesis_block = create_genesis_block()
print(f"Genesis Block Hash: {genesis_block.hash}")

# Add function to generate new blocks
def create_new_block(previous_block, data):
    index = previous_block.index + 1
    timestamp = time.time()
    previous_hash = previous_block.hash
    return Block(index, timestamp, data, previous_hash)

# Test block creation
new_block = create_new_block(genesis_block, "First transaction data")
print(f"New Block Hash: {new_block.hash}")