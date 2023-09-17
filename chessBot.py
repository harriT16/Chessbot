import tkinter as tk
from tkinter import ttk
import chess
import chess.svg
import random
from PIL import Image, ImageTk
import cairosvg
import io

class ChessApp:
    def __init__(self, master):
        self.board = chess.Board()
        self.master = master
        self.master.title("Simple Chess Bot")
        
        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()
        
        self.refresh_board()
        
        ttk.Label(self.master, text="Enter your move:").pack()
        self.move_entry = ttk.Entry(self.master)
        self.move_entry.pack()
        
        ttk.Button(self.master, text="Make Move", command=self.make_move).pack()
        
    def make_move(self):
        user_move = self.move_entry.get()
        if chess.Move.from_uci(user_move) in self.board.legal_moves:
            self.board.push(chess.Move.from_uci(user_move))
            self.refresh_board()
            
            if not self.board.is_game_over():
                bot_move = self.get_bot_move()
                self.board.push(bot_move)
                print(f"Bot plays {bot_move.uci()}")
                self.refresh_board()
            
            if self.board.is_game_over():
                print("Game over")
                print("Result: " + self.board.result())
                
    def refresh_board(self):
        img_data = chess.svg.board(self.board).encode("UTF-8")
        png_data = cairosvg.svg2png(bytestring=img_data)
        image = Image.open(io.BytesIO(png_data))
        self.img = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)
        
    def get_bot_move(self):
        legal_moves = [move for move in self.board.legal_moves]
        return random.choice(legal_moves)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
