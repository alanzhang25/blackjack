import tkinter as tk
import random, time
from PIL import Image, ImageTk
from typing import List

class Player:
    def __init__(self, name, frame: tk.LabelFrame, amount):
        self.name = name
        self.frame = frame
        self.hands = [] 
        self.current_amount = amount

    def reset_hand(self):
        self.hands = []

class Hand:
    def __init__(self, player: Player = None):
        self.num_aces = 0
        self.count = 0
        self.prev_value = 0
        self.blackjack = False
        self.split = False
        self.images_list = []

        if player:
            self.player = player
            self.frame = tk.Frame(player.frame, padx=2, pady=2, bg="green")
            self.frame.grid(row=1, column=len(player.hands), padx=2, pady=2, sticky="w")
            self.label_frame = tk.Frame(player.frame, bg="green")
            self.label_frame.grid(row=2, column=len(player.hands), sticky="w")

    def split_hand(self):
        s_hand = Hand(self.player)
        global_hands.append(s_hand)

        if self.num_aces > 0:
            self.num_aces = 1
            self.count = 11
            s_hand.num_aces = 1
            s_hand.count = 11
        else:
            self.count = self.count / 2
            s_hand.count = self.count
        
        self.split = False
        c_image = self.images_list.pop()
        s_hand.images_list.append(c_image)
        card_labels = tk.Label(s_hand.frame, image=c_image, bg="green")
        self.player.hands.append(s_hand)
        card_labels.pack(side="left")

        # frame = tk.LabelFrame(root, text=f"Player Split", padx=10, pady=10, bg="green", fg="white")
        # frame.grid(row=1, column=len(self.player.hands) + 1, padx=10, pady=10, sticky="w")
        # player.split_frame.append(frame)

        # remove card from first
        for widget in self.frame.winfo_children():
            widget.destroy()

        card_labels = tk.Label(self.frame, image=self.images_list[0], bg="green")
        card_labels.pack(side="left")

    def add_card(self, path):
        value = int(path.split("_")[0])
        if value == self.prev_value and len(self.images_list) < 3:
            self.split = True
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
        
        self.prev_value = value

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
        players.append(Player("Player {i}", frame, 100))
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
    card_labels.pack(side="left")

    if hand.count >= 9 and hand.count <= 11 and len(hand.images_list) == 2:
        double_button.config(state="normal")
    
    if hand.split:
        split_button.config(state="normal")

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
    card_label.pack(side="left")

def hidden_hit(dealer: Dealer):
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    global hidden_image
    hidden_image = resize_cards("back")
    dealer.images_list.append(card_image)
    dealer.hand.add_card(card)
    card_label = tk.Label(dealer.frame, image=hidden_image, bg="green")
    card_label.pack(side="left")
    return card_image, card_label

def stand(player_bust=False):
    global global_hands, hand_index
    hand_index += 1


    def dealer_play():
        if (dealer.hand.count < 17 or (dealer.hand.count == 17 and dealer.hand.num_aces > 0)) and not player_bust:
            dealer_hit(dealer)
            print(dealer.hand.count)
            root.after(1000, dealer_play)
        else:
            print("Dealer stands.")
            end_logic()

    if hand_index >= len(global_hands):
        root.after(1000, lambda: card_label.config(image=card_image))
        print(dealer.hand.count)
        root.after(2000, dealer_play)
    else:
        global_hands[hand_index-1].frame.config(bg="green")
        global_hands[hand_index].frame.config(bg="#FFFFC0")

def player_double(hand : Hand):
    """Add a card to the specified player's frame."""
    card = random.choice(deck)
    deck.remove(card)
    card_image = resize_cards(card)
    hand.images_list.append(card_image)
    hand.add_card(card)
    card_labels = tk.Label(hand.frame, image=card_image, bg="green")
    card_labels.pack(side="left")

    double_button.config(state="disabled")
    global bet_amount
    bet_amount = bet_amount * 2

    if hand.count == 21 and not hand.blackjack:
        stand()
    elif hand.count > 21:
        stand(player_bust=True)
    else:
        stand()

def player_split(hand : Hand):
    hand.split_hand()
    split_button.config(state="disabled")

def end_logic():
    d_count = dealer.hand.count
    for player in players:
        for hand in player.hands:
            p_count = hand.count
            if dealer.hand.blackjack:
                result_text = "Dealer Blackjack"
                players[0].current_amount -= bet_amount
            elif hand.blackjack:
                result_text = "Blackjack!"
                players[0].current_amount += (bet_amount * 1.5)
            elif p_count > 21:
                result_text = "Bust"
                players[0].current_amount -= bet_amount
            elif d_count > 21:
                result_text = "Win (Dealer Bust)"
                players[0].current_amount += bet_amount
            elif p_count > d_count:
                result_text = "Win!"
                players[0].current_amount += bet_amount
            elif p_count < d_count:
                result_text = "Lose"
                players[0].current_amount -= bet_amount
            else:
                result_text = "Tie"

            total_amount.config(text="Total Amount : " + str(players[0].current_amount))
            label = tk.Label(hand.label_frame, text=result_text, bg="green")
            label.grid(row=0, column=0)
    
    def remove_cards():
        for player in players:
            for widget in player.frame.winfo_children():
                widget.destroy()
        
        for widget in dealer.frame.winfo_children():
                widget.destroy()

        global bet_amount
        bet_amount = 10
        counter_label.config(text="Bet Amount : " + str(bet_amount))

        player.reset_hand()
        dealer.reset_hand()
        global global_hands, hand_index
        global_hands = []
        hand_index = 0

        double_button.config(state="disabled")
        split_button.config(state="disabled")

        if len(deck) < 10:
            shuffle_label = tk.Label(root, text="Shuffling", font=("Helvetica", 24), bg="green", fg="white")
            shuffle_label.place(relx=0.5, rely=0.5, anchor="center")
            root.after(2000, shuffle_label.destroy)
            root.after(2000, shuffle)
    
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
    
    global_hands[0].frame.config(bg='#FFFFC0')

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
global split_button
split_button = tk.Button(button_frame, text="Split", font=("Helvetica", 14), state="disabled", command=lambda: player_split(global_hands[hand_index]))
split_button.grid(row=0, column=4)
shuffle_button = tk.Button(button_frame, text="Shuffle", font=("Helvetica", 14), command=lambda: shuffle)
shuffle_button.grid(row=0, column=0)


bet_frame = tk.Frame(root, bg="green")
bet_frame.grid(row=4, column=6, pady=100, sticky='n')

bet_amount = 10
total_amount = tk.Label(bet_frame, text="Total Amount : " + str(players[0].current_amount), bg="green", font=("Arial", 16))
total_amount.pack(side='top', pady=30)
counter_label = tk.Label(bet_frame, text="Bet Amount : " + str(bet_amount), bg="green", font=("Arial", 16))
counter_label.pack()

def increase(amount):
    global bet_amount
    bet_amount += amount
    counter_label.config(text="Bet Amount : " + str(bet_amount))

five_btn = tk.Button(bet_frame, text="5", font=("Arial", 14), bg="green", command=lambda: increase(5))
five_btn.pack(side="left")
ten_btn = tk.Button(bet_frame, text="10", font=("Arial", 14), bg="green", command=lambda: increase(10))
ten_btn.pack(side="left")
confirm_btn = tk.Button(bet_frame, text="Confirm", font=("Arial", 14), bg="green", command= starting_hand)
confirm_btn.pack(side="left")

starting_hand()
# Run the main event loop
root.mainloop()

