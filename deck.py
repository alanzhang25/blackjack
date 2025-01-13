import tkinter as tk
import random
from PIL import Image, ImageTk



class Card:
    def __init__(self, path):
        self.path
        value = int(path.split("_")[0])
        if value == 1:
            self.value = 11
        elif value == 11 or value == 12 or value == 13:
            self.value = 10
        else:
            self.value = value

class Hand:
    def __init__(self):
        self.cards = []
        self.count = 0

class Dealer:
    def __init__(self, frame):
        self.name = "Dealer"
        self.hand = []
        self.frame = frame
        self.images_list = []
        self.count = Hand()

    def add_card(self, card):
        self.hand.append(card)

class Player:
    def __init__(self, name, frame):
        self.name = name
        self.hand = []
        self.frame = frame
        self.images_list = []
        self.count = Hand()

    def add_card(self, card):
        self.hand.append(card)            

def resize_cards(card):
	our_card_img = Image.open(f"cards/{card}.png")

	our_card_resize_image = our_card_img.resize((80, 120))

	our_card_image = ImageTk.PhotoImage(our_card_resize_image)

	return our_card_image

def shuffle():
    suits = ["diamonds", "clubs", "hearts", "spades"]
    values = range(1, 14) # 1 Ace, 11 Jack, 12 Queen, 13 King

    global deck
    deck = []

    for suit in suits:
        for value in values:
            deck.append(f'{value}_of_{suit}')
    

def create_players(root, num_players):
    """Dynamically create player frames based on the number of players."""
    players = []
    for i in range(num_players):
        frame = tk.LabelFrame(root, text=f"Player {i + 1}", padx=10, pady=10, bg="green", fg="white")
        frame.grid(row=1, column=i, padx=10, pady=10)
        players.append(Player("Player {i}", frame))
    return players

def player_hit(player : Player):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    player.images_list.append(card_image)
    card_label = tk.Label(player.frame, image=card_image, bg="green")
    card_label.pack(side="left", padx=5)

def dealer_hit(dealer: Dealer):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    dealer.images_list.append(card_image)
    card_label = tk.Label(dealer.frame, image=card_image, bg="green")
    card_label.pack(side="left", padx=5)

class Game:
    def __init__(self, num_players):
        dealer = Dealer()
        players = []
        for i in num_players:
            players.append(Player(f"Player {i}"))

# Main application window
root = tk.Tk()
root.title("Blackjack")
root.geometry("1000x800")
root.configure(background="green")

dealer_frame = tk.LabelFrame(root, text="Dealer", padx=10, pady=10, bg="green", fg="white")
dealer_frame.grid(row=0, column=0, padx=10, pady=20)
dealer = Dealer(dealer_frame)

shuffle()
dealer_hit(dealer)
dealer_hit(dealer)

# Create player frames
players= create_players(root, 4)

player_hit(players[0])
player_hit(players[1])
player_hit(players[2])
player_hit(players[2])
player_hit(players[3])
player_hit(players[3])

# Run the main event loop
root.mainloop()

