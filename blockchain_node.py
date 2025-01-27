import hashlib
import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Used for Proof-of-Work
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Hash includes the index, timestamp, data, previous hash, and nonce
        data_to_hash = (
            str(self.index) +
            str(self.timestamp) +
            self.data +
            self.previous_hash +
            str(self.nonce)
        )
        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    def mine_block(self, difficulty):
        # Proof-of-Work algorithm: Adjust nonce until the hash starts with difficulty zeros
        target = "0" * difficulty
        print(f"Mining block {self.index}...")
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} successfully mined: {self.hash}")


class Blockchain:
    def __init__(self, difficulty=2):  # Default difficulty is 2
        self.difficulty = difficulty  # Difficulty for mining
        self.chain = [self.create_genesis_block()]  # Initialize with the genesis block

    def create_genesis_block(self):
        # Create the genesis block (index 0, arbitrary data, no previous hash)
        print("Creating genesis block...")
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        return genesis_block

    def get_latest_block(self):
        # Return the last block in the chain
        return self.chain[-1]

    def add_block(self, data):
        # Create a new block and add it to the chain
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, latest_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)


class Node:
    def __init__(self, name, difficulty=2):
        self.name = name
        self.blockchain = Blockchain(difficulty)

    def add_block_to_chain(self, data):
        print(f"[{self.name}] Adding block with data: {data}")
        self.blockchain.add_block(data)

    def print_chain(self):
        print(f"\n[{self.name}] Blockchain:")
        for block in self.blockchain.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Hash: {block.hash}")
            print(f"Nonce: {block.nonce}")
            print("-" * 50)


# Main script to test the Node and Blockchain
if __name__ == "__main__":
    # Create a Node with a specified difficulty
    node_a = Node("Node A", difficulty=2)

    # Add blocks to the blockchain
    node_a.add_block_to_chain("First block data")
    node_a.add_block_to_chain("Second block data")
    node_a.add_block_to_chain("Third block data")

    # Print the blockchain
    node_a.print_chain()
