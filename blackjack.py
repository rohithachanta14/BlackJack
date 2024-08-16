import random

# Defining card suits, ranks, and values
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
card_values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
               'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}

game_in_progress = True

# Card deck class
class Deck:
    def __init__(self):
        self.cards = []  # Start with an empty list
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))  # Build Card objects and add them to the list

    def __str__(self):
        deck_composition = ''  # Start with an empty string
        for card in self.cards:
            deck_composition += '\n ' + card.__str__()  # Add each Card object's print string
        return 'The deck has:' + deck_composition

    def shuffle(self):
        random.shuffle(self.cards)
        
    def deal(self):
        return self.cards.pop()

# Player's hand class
class Hand:
    def __init__(self):
        self.cards_in_hand = []  # Start with an empty list
        self.total_value = 0   # Start with zero value
        self.aces_in_hand = 0   # Add an attribute to keep track of aces
    
    def add_card(self, card):
        self.cards_in_hand.append(card)
        self.total_value += card_values[card.rank]
    
    def adjust_for_ace(self):
        while self.total_value > 21 and self.aces_in_hand:
            self.total_value -= 10
            self.aces_in_hand -= 1

# Chips class to manage player's betting chips
class Chips:
    def __init__(self):
        self.total_chips = 100  # Default value
        self.bet_amount = 0
        
    def win_bet(self):
        self.total_chips += self.bet_amount
    
    def lose_bet(self):
        self.total_chips -= self.bet_amount

# Function to take bet from player
def take_bet(chips):
    while True:
        try:
            chips.bet_amount = int(input('How many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet_amount > chips.total_chips:
                print("Sorry, your bet can't exceed", chips.total_chips)
            else:
                break

# Function to hit (add a card to the player's hand)
def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# Function to ask player if they want to hit or stand
def hit_or_stand(deck, hand):
    global game_in_progress  # to control an upcoming while loop
    
    while True:
        player_choice = input("Would you like to Hit or Stand? Enter 'h' or 's' ")
        
        if player_choice[0].lower() == 'h':
            hit(deck, hand)  # hit() function defined above

        elif player_choice[0].lower() == 's':
            print("Player stands. Dealer is playing.")
            game_in_progress = False

        else:
            print("Sorry, please try again.")
            continue
        break

# Function to show some cards (partially hide dealer's hand)
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards_in_hand[1])  
    print("\nPlayer's Hand:", *player.cards_in_hand, sep='\n ')
    
# Function to show all cards
def show_all(player, dealer):
    print("\nDealer's Hand:", *dealer.cards_in_hand, sep='\n ')
    print("Dealer's Hand =", dealer.total_value)
    print("\nPlayer's Hand:", *player.cards_in_hand, sep='\n ')
    print("Player's Hand =", player.total_value)

# Functions to handle different game outcomes
def player_busts(player, dealer, chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player, dealer):
    print("Dealer and Player tie! It's a push.")


### Game Play ###
while True:
    # Print an opening statement
    print('Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
    Dealer hits until she reaches 17. Aces count as 1 or 11.')
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
            
    # Set up the Player's chips
    player_chips = Chips()  # Default value is 100    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand, dealer_hand)
    
    while game_in_progress:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand) 
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)  
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.total_value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break        

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 
    if player_hand.total_value <= 21:
        
        while dealer_hand.total_value < 17:
            hit(deck, dealer_hand)    
    
        # Show all cards
        show_all(player_hand, dealer_hand)
        
        # Run different winning scenarios
        if dealer_hand.total_value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.total_value > player_hand.total_value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.total_value < player_hand.total_value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)        
    
    # Inform Player of their chips total 
    print("\nPlayer's winnings stand at", player_chips.total_chips)
    
    # Ask to play again
    new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
    
    if new_game[0].lower() == 'y':
        game_in_progress = True
        continue
    else:
        print("Thanks for playing!")
        break
