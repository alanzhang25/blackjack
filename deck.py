import tkinter as tk
import random, time
from PIL import Image, ImageTk
from typing import List

class Player:
    def __init__(self, name, frame: tk.LabelFrame):
        self.name = name
        self.frame = frame
        self.hands = [] 

    def reset_hand(self):
        self.hands = []

class Hand:
    def __init__(self, player: Player = None):
        self.num_aces = 0
        self.count = 0
        self.blackjack = False
        self.images_list = []

        if player:
            self.player = player
            self.frame = tk.Frame(player.frame, padx=10, pady=10, bg="green")
            self.frame.grid(row=1, column=len(player.hands), padx=10, pady=10, sticky="w")

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

def player_hit(hand: Hand):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    # card = "8_of_hearts"
    card_image = resize_cards(card)
    hand.images_list.append(card_image)
    hand.add_card(card)
    card_labels = tk.Label(hand.frame, image=card_image, bg="green")
    card_labels.pack(side="left", padx=1)

    if hand.count == 21 and not hand.blackjack:
        stand()
    elif hand.count > 21:
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
    global global_hands, hand_index
    hand_index += 1
    root.after(1000, lambda: card_label.config(image=card_image))
    print(dealer.hand.count)

    def dealer_play():
        if (dealer.hand.count < 17 or (dealer.hand.count == 17 and dealer.hand.num_aces > 0)) and not player_bust:
            dealer_hit(dealer)
            print(dealer.hand.count)
            root.after(1000, dealer_play)
        elif hand_index >= len(global_hands):
            print("Dealer stands.")
            end_logic()

    root.after(2000, dealer_play)

def player_double(hand : Hand):
    """Add a card to the specified player's frame."""
    global global_hands, hand_index
    hand_index += 1
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    hand.images_list.append(card_image)
    hand.add_card(card)
    card_labels = tk.Label(hand.frame, image=card_image, bg="green")
    card_labels.pack(side="left", padx=1)

    if hand.count == 21 and not hand.blackjack:
        stand()
    elif hand.count > 21:
        stand(player_bust=True)
    else:
        stand()

# def player_split(player : Player):
#         frame = tk.LabelFrame(root, text=f"Player Split", padx=10, pady=10, bg="green", fg="white")
#         frame.grid(row=1, column=len(player.split_hands) + 1, padx=10, pady=10, sticky="w")
#         player.split_frame.append(frame)

#         # remove card from first
#         for widget in player.frame.winfo_children():
#             widget.destroy()

#         card_labels = tk.Label(player.frame, image=player.images_list[0], bg="green")
#         card_labels.pack(side="left", padx=1)

#         card_labels2 = tk.Label(player.split_frame[len(player.split_hands)], image=player.images_list[1], bg="green")
#         card_labels2.pack(side="left", padx=1)

#         player.split_hand()
#         print(len(player.split_hands))

def end_logic():
    d_count = dealer.hand.count
    for player in players:
        for hand in player.hands:
            p_count = hand.count
            if dealer.hand.blackjack:
                result_text = "Dealer Blackjack"
            elif hand.blackjack:
                result_text = "Blackjack!"
            elif p_count > 21:
                result_text = "Bust"
            elif d_count > 21:
                result_text = "Win (Dealer Bust)"
            elif p_count > d_count:
                result_text = "Win!"
            elif p_count < d_count:
                result_text = "Lose"
            else:
                result_text = "Tie"

            label = tk.Label(hand.frame, text=result_text, bg="green")
            label.pack(side="bottom", padx=1)
    
    def remove_cards():
        for player in players:
            for widget in player.frame.winfo_children():
                widget.destroy()
        
        for widget in dealer.frame.winfo_children():
                widget.destroy()

        player.reset_hand()
        dealer.reset_hand()
        global global_hands, hand_index
        global_hands = []
        hand_index = 0
        


        double_button.config(state="disabled")

        if len(deck) < 10:
            shuffle_label = tk.Label(root, text="Shuffling", font=("Helvetica", 24), bg="green", fg="white")
            shuffle_label.place(relx=0.5, rely=0.5, anchor="center")
            root.after(2000, shuffle_label.destroy)
            root.after(2000, shuffle)
            root.after(2500, starting_hand)
        else:
            root.after(500, starting_hand)
    
    root.after(2000, remove_cards)


def starting_hand():
    dealer_hit(dealer)
    global card_image, card_label
    card_image, card_label = hidden_hit(dealer)

    for player in players:
        hand = Hand(player)
        player.hands.append(hand)
        global global_hands, hand_index
        global_hands.append(hand)
        player_hit(hand)
        player_hit(hand)

    for player in players:
        for hand in player.hands:
            if hand.count == 21:
                hand.blackjack = True

    if dealer.hand.count == 21:
        dealer.hand.blackjack 
    
    if players[0].hands[0].count >= 9 and players[0].hands[0].count <= 11:
        double_button.config(state="normal")

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

dealer_frame = tk.LabelFrame(root, text="Dealer", bg="green", fg="white",padx=10, pady=10)
dealer_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

dealer = Dealer(dealer_frame)

shuffle()
global global_hands
global_hands = []
global hand_index
hand_index = 0
players= create_players(root, 1)

button_frame = tk.Frame(root, background="green", bd=0)
button_frame.grid(row=3, sticky="w")
card_button = tk.Button(button_frame, text="Hit", font=("Helvetica", 14), command=lambda: player_hit(global_hands[hand_index]))
card_button.grid(row=0, column=1)
stand_button = tk.Button(button_frame, text="Stand", font=("Helvetica", 14), command=lambda: stand())
stand_button.grid(row=0, column=2)
global double_button
double_button = tk.Button(button_frame, text="Double", font=("Helvetica", 14), state="disabled", command=lambda: player_double(global_hands[hand_index]))
double_button.grid(row=0, column=3)
shuffle_button = tk.Button(button_frame, text="Shuffle", font=("Helvetica", 14), command=lambda: shuffle)
shuffle_button.grid(row=0, column=0)

starting_hand()


# Run the main event loop
root.mainloop()

