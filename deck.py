import tkinter as tk
import random, time
from PIL import Image, ImageTk
from typing import List

class Hand:
    def __init__(self):
        self.num_aces = 0
        self.count = 0
        self.blackjack = False

    def add_card(self, path):
        value = int(path.split("_")[0])
        if value == 1:
            self.num_aces += 1
            if self.count < 11:
                self.count += 11
            else:
                self.num_aces -= 1
                self.count += 1
        elif value == 11 or value == 12 or value == 13:
            self.count += 10
        else:
            self.count += value

        if self.count > 21 and self.num_aces > 0:
            self.num_aces -= 1
            self.count -= 10

class Dealer:
    def __init__(self, frame):
        self.name = "Dealer"
        self.frame = frame
        self.images_list = []
        self.hand = Hand()
    
    def reset_hand(self):
        self.hand = Hand()
        self.images_list = []   

class Player:
    def __init__(self, name, frame: tk.LabelFrame):
        self.name = name
        self.frame = frame
        self.images_list = []
        self.hand = Hand()      

    def reset_hand(self):
        self.hand = Hand()
        self.images_list = []   

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
    

def create_players(root, num_players) -> List[Player]:
    """Dynamically create player frames based on the number of players."""
    players = []
    for i in range(num_players):
        frame = tk.LabelFrame(root, text=f"Player {i + 1}", padx=10, pady=10, bg="green", fg="white")
        frame.grid(row=1, column=i, padx=10, pady=10, sticky="w")
        players.append(Player("Player {i}", frame))
    return players

def player_hit(player : Player):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    player.images_list.append(card_image)
    player.hand.add_card(card)
    card_labels = tk.Label(player.frame, image=card_image, bg="green")
    card_labels.pack(side="left", padx=1)

    if player.hand.count == 21 and not player.hand.blackjack:
        stand()
    elif player.hand.count > 21:
        stand(player_bust=True)

def dealer_hit(dealer: Dealer):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    dealer.images_list.append(card_image)
    dealer.hand.add_card(card)
    card_label = tk.Label(dealer.frame, image=card_image, bg="green")
    card_label.pack(side="left", padx=1)

def hidden_hit(dealer: Dealer):
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    global hidden_image
    hidden_image = resize_cards("back")
    dealer.images_list.append(card_image)
    dealer.hand.add_card(card)
    card_label = tk.Label(dealer.frame, image=hidden_image, bg="green")
    card_label.pack(side="left", padx=1)
    return card_image, card_label

def stand(player_bust=False):
    root.after(1000, lambda: card_label.config(image=card_image))
    print(dealer.hand.count)

    def dealer_play():
        if (dealer.hand.count < 17 or (dealer.hand.count == 17 and dealer.hand.num_aces > 0)) and not player_bust:
            dealer_hit(dealer)
            print(dealer.hand.count)
            root.after(1000, dealer_play)
        else:
            print("Dealer stands.")
            end_logic()

    root.after(2000, dealer_play)

def end_logic():
    d_count = dealer.hand.count
    for player in players:
        p_count = player.hand.count
        if player.hand.blackjack:
            label = tk.Label(player.frame, text="Blackjack!", bg="green")
            label.pack(side="bottom", padx=1)
        elif p_count > 21:
            label = tk.Label(player.frame, text="Lose", bg="green")
            label.pack(side="bottom", padx=1)
        elif p_count > d_count or d_count > 21:
            # player wins
            label = tk.Label(player.frame, text="Win!", bg="green")
            label.pack(side="bottom", padx=1)
        elif p_count < d_count:
            label = tk.Label(player.frame, text="Lose", bg="green")
            label.pack(side="bottom", padx=1)
        else:
            label = tk.Label(player.frame, text="Tie", bg="green")
            label.pack(side="bottom", padx=1)
    
    def remove_cards():
        for player in players:
            for widget in player.frame.winfo_children():
                widget.destroy()
        
        for widget in dealer.frame.winfo_children():
                widget.destroy()

        player.reset_hand()
        dealer.reset_hand()

        root.after(500, starting_hand)
    
    root.after(2000, remove_cards)


def starting_hand():
    dealer_hit(dealer)
    global card_image, card_label
    card_image, card_label = hidden_hit(dealer)
    player_hit(players[0])
    player_hit(players[0])

    for player in players:
        if player.hand.count == 21:
            player.hand.blackjack = True

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

dealer_frame = tk.LabelFrame(root, text="Dealer", bg="green", fg="white")
dealer_frame.grid(row=0, column=0, padx=10, pady=20, sticky="w")

dealer = Dealer(dealer_frame)

shuffle()
players= create_players(root, 1)

button_frame = tk.Frame(root, bg="green")
button_frame.grid(pady=20, row=3, sticky="w")
card_button = tk.Button(button_frame, text="Hit", font=("Helvetica", 14), command=lambda: player_hit(players[0]))
card_button.grid(row=0, column=1, padx=10)

starting_hand()

stand_button = tk.Button(button_frame, text="Stand", font=("Helvetica", 14), command=lambda: stand())
stand_button.grid(row=0, column=2)
shuffle_button = tk.Button(button_frame, text="Shuffle Deck", font=("Helvetica", 14), command=lambda: shuffle)
shuffle_button.grid(row=0, column=0)


# Run the main event loop
root.mainloop()

