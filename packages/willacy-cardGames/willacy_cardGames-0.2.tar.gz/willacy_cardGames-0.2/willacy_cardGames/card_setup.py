class Card:
    
    suits = ["Clubs", "Diamonds", "Hearts", "Spades"]
    ranks = ["narf", "Ace", "2", "3", "4", "5", "6", "7",
             "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=0):
        self.suit = suit
        self.rank = rank
    
    # print out card rank and suit
    def __str__(self):
        return (self.ranks[self.rank] + " of " + self.suits[self.suit])
    
   # compare cards
    def cmp(self, other):
        # Check the suits
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        # Suits are the same... check ranks
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # Ranks are the same... it's a tie
        return 0
    
    
    def __eq__(self, other): # ie. a == b
        return self.cmp(other) == 0

    def __le__(self, other): # ie. a <= b
        return self.cmp(other) <= 0

    def __ge__(self, other): # ie. a >= b
        return self.cmp(other) >= 0

    def __gt__(self, other): # ie. a > b
        return self.cmp(other) > 0

    def __lt__(self, other): # ie. a < b
        return self.cmp(other) < 0

    def __ne__(self, other): # ie. a != b
        return self.cmp(other) != 0
    
class Deck:
    
    """
    Populates a deck of cards by cycling through all 
    the cards in Card class.
    """
    
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))
            
    # prints out every card currently in the deck
    def print_deck(self):
        for card in self.cards:
            print(card)
            
    # alternative to print_deck which prints one long string with an additional
    # space and new line after each card.
    def __str__(self):
        s = ""
        for i in range(len(self.cards)):
            s = s + " " * i + str(self.cards[i]) + "\n"
        return s
    
    # shuffles the deck
    def shuffle(self):
        import random
        rng = random.Random()        # Create a random generator
        num_cards = len(self.cards)
        for i in range(num_cards):
            j = rng.randrange(i, num_cards)
            (self.cards[i], self.cards[j]) = (self.cards[j], self.cards[i])
            
    
    # remove card from deck
    def remove(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    
    # removes card from end of list
    def pop(self):
        return self.cards.pop()
    
    # checks if the deck has any cards left
    def is_empty(self):
        return self.cards == []
    
    # dealing the hand
    def deal(self, hands, num_cards=999):
        num_hands = len(hands)
        for i in range(num_cards):
            if self.is_empty():
                break                    # Break if out of cards in the deck
            card = self.pop()            # Take the top card
            hand = hands[i % num_hands]  # Deals to each hand one by one
            hand.add(card)     
    
    
class Hand(Deck):
    
    """
    Inherits from Deck class. 
    For when dealing a hand to players.
    """
    
    def __init__(self, name=""):
       self.cards = []
       self.name = name
    
    # adds card to Hand
    def add(self, card):
        self.cards.append(card)
    
    # print function to override Deck function
    def __str__(self):
        s = "Hand " + self.name
        if self.is_empty():
            s += " is empty\n"
        else:
            s += " contains\n"
        return s + Deck.__str__(self)
    
class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
