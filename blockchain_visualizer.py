import hashlib
import time
import tkinter as tk
from tkinter import messagebox
from threading import Thread


class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        to_hash = (
            str(self.index)
            + str(self.timestamp)
            + self.data
            + self.previous_hash
            + str(self.nonce)
        )
        return hashlib.sha256(to_hash.encode()).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self, difficulty=2):
        self.difficulty = difficulty
        self.chain = [self.create_genesis_block()]
        self.mining_in_progress = False

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        genesis_block.mine_block(self.difficulty)
        return genesis_block

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(len(self.chain), time.time(), data, latest_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def start_mining(self):
        self.mining_in_progress = True

    def stop_mining(self):
        self.mining_in_progress = False


class BlockchainVisualizer(tk.Tk):
    def __init__(self, blockchain):
        super().__init__()
        self.blockchain = blockchain
        self.title("Blockchain Visualization")
        self.geometry("900x700")

        # Canvas for drawing the blocks
        self.canvas = tk.Canvas(self, bg="#f0f8ff", width=900, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Difficulty slider and label
        self.difficulty_label = tk.Label(self, text="Set Mining Difficulty: ", font=("Helvetica", 14, "bold"))
        self.difficulty_label.pack(pady=10)

        self.difficulty_slider = tk.Scale(self, from_=1, to=5, orient=tk.HORIZONTAL, font=("Helvetica", 12))
        self.difficulty_slider.set(self.blockchain.difficulty)
        self.difficulty_slider.pack()

        # Buttons for adding blocks and starting/stopping mining
        self.add_block_button = tk.Button(
            self, text="Add Block", command=self.add_block, font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white"
        )
        self.add_block_button.pack(pady=20)

        self.mine_button = tk.Button(
            self, text="Start Mining", command=self.toggle_mining, font=("Helvetica", 12, "bold"), bg="#FF6347", fg="white"
        )
        self.mine_button.pack(pady=10)

        # Mining status label
        self.mine_status_label = tk.Label(self, text="Mining Status: Stopped", font=("Arial", 14))
        self.mine_status_label.pack(pady=10)

    def draw_blockchain(self):
        self.canvas.delete("all")  # Clear previous drawings

        start_x = 50
        start_y = 100
        block_width = 250
        block_height = 150
        spacing_x = 300
        spacing_y = 200
        max_blocks_per_row = 3

        for i, block in enumerate(self.blockchain.chain):
            x = start_x + (i % max_blocks_per_row) * spacing_x
            y = start_y + (i // max_blocks_per_row) * spacing_y

            self.canvas.create_rectangle(x, y, x + block_width, y + block_height, fill="#87CEEB", outline="black")
            self.canvas.create_text(x + block_width / 2, y + 20, text=f"Block {block.index}", font=("Arial", 14, "bold"), fill="darkblue")
            self.canvas.create_text(x + block_width / 2, y + 40, text=f"Data: {block.data}", font=("Arial", 12), fill="darkgreen")
            self.canvas.create_text(x + block_width / 2, y + 80, text=f"Hash: {block.hash[:20]}...", font=("Courier New", 10), fill="darkred", width=block_width - 20)
            self.canvas.create_text(x + block_width / 2, y + 100, text=f"Prev: {block.previous_hash[:20]}...", font=("Courier New", 10), fill="darkorange", width=block_width - 20)

            if i > 0:
                prev_x = start_x + ((i - 1) % max_blocks_per_row) * spacing_x
                prev_y = start_y + ((i - 1) // max_blocks_per_row) * spacing_y
                self.canvas.create_line(prev_x + block_width, prev_y + block_height / 2, x, y + block_height / 2, arrow=tk.LAST, fill="gray")

    def add_block(self):
        self.blockchain.difficulty = self.difficulty_slider.get()
        self.blockchain.add_block("New Block Data")
        self.draw_blockchain()

    def toggle_mining(self):
        if self.blockchain.mining_in_progress:
            self.blockchain.stop_mining()
            self.mine_button.config(text="Start Mining", bg="#FF6347", fg="white")
            self.mine_status_label.config(text="Mining Status: Stopped", fg="red")
        else:
            self.blockchain.start_mining()
            self.mine_button.config(text="Stop Mining", bg="#4CAF50", fg="white")
            self.mine_status_label.config(text="Mining Status: Running", fg="green")
            Thread(target=self.mine_in_background, daemon=True).start()

    def mine_in_background(self):
        while self.blockchain.mining_in_progress:
            self.add_block()
            time.sleep(1)

    def display_instructions(self):
        instructions = (
            "Instructions for using the Blockchain Visualizer:\n\n"
            "1. Set Mining Difficulty using the slider.\n"
            "2. Click 'Add Block' to manually add a new block to the blockchain.\n"
            "3. Click 'Start Mining' to begin mining and automatically adding blocks.\n"
            "4. To stop mining, click 'Stop Mining'.\n\n"
            "You can observe how blocks are added to the chain in real-time!"
        )
        messagebox.showinfo("Instructions", instructions)


def run_visualizer():
    blockchain = Blockchain()
    visualizer = BlockchainVisualizer(blockchain)
    visualizer.draw_blockchain()
    visualizer.after(1000, visualizer.display_instructions)
    visualizer.mainloop()


if __name__ == "__main__":
    run_visualizer()
