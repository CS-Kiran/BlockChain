import hashlib
import time

# Define the Block class
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Combine the block's data to create its hash
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


# Define the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # The first block in the blockchain
        return Block(0, time.time(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        # Add a new block to the chain
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, previous_block.hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Verify the integrity of the blockchain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the block links to the correct previous block
            if current_block.previous_hash != previous_block.hash:
                return False

        return True


# Create a blockchain and add some blocks
my_blockchain = Blockchain()
my_blockchain.add_block("Block 1 Data")
my_blockchain.add_block("Block 2 Data")
my_blockchain.add_block("Block 3 Data")

# Print the blockchain
for block in my_blockchain.chain:
    print(f"Index: {block.index}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Data: {block.data}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Hash: {block.hash}")
    print("-" * 50)

# Check if the blockchain is valid
print("Is blockchain valid?", my_blockchain.is_chain_valid())
