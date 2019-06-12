# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:

import random
import pdb

#global variables
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

b_playing = True
# CLASS DEFINTIONS:

class Card: # will create a single card object
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        the_card = ''
        the_card = f'{self.rank} of {self.suit}'
        return the_card


class Deck: #will create a deck of card objects   
    def __init__(self):
        
        self.this_deck = []
        
        for r in ranks:
            for s in suits:
                self.this_deck.append(Card(r,s))

    def __str__(self):
        cards_in_deck = ''
        for c in self.this_deck:
            cards_in_deck += '\n' + c.__str__()
        return cards_in_deck

    def shuffle(self):
        random.shuffle(self.this_deck)

    def deal(self):
        card_dealt = self.this_deck.pop() #pops out a Card() object
        return card_dealt #returns the card object



class Hand:
    def __init__(self,who='Player'):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        self.who  = who  # optional pass so we know who's hand we are dealing with
        self.busted = 'False'
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        if card.rank == 'Ace':
            self.aces +=1

    def adjust_for_ace(self):
        while self.aces > 0:
            if self.value > 21:
                self.value -= 10
                self.aces  -= 1
            else:
                break

    def __str__(self):
        cards_in_hand = ''
        for c in self.cards:
            cards_in_hand += '\n '+ c.__str__()
        return '\n' + self.who +'\'s Hand:\n' + cards_in_hand 


class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win(self):
        self.total += self.bet

    def lose(self):
        self.total -= self.bet
        



# FUNCTION DEFINITIONS:

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('\nHow many chips would you like to bet? '))
        except ValueError:
            print('Sorry, a bet must be an integer!')
        else:
            if chips.bet > chips.total:
                print("Sorry, your bet can't exceed",chips.total)
                continue
            elif chips.bet > 100:
                print("Sorry the table limit is 100")
                continue
            elif chips.bet < 20:
                print("Sorry the table minimum is 20")
                continue
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck,hand):
    
    if hand.who == 'Player':
        response = ''
        while not (response == 'S'):
            response = input('\nEnter H to Hit or S to Stand: ').upper()

            if not (response == 'H' or response == 'S'):
                print('\nYou can only enter H or S')
                continue

            if response == 'H':
                hit(deck,hand)
                print(hand.__str__()) # pass the hand to be printed
                print('\n Hand Value: ',hand.value)

                if hand.value > 21:
                    busts(hand)
                    break
                elif hand.value == 21:
                    response = 'S'
                    break
            elif response == 'S':
                break
    else:
        while hand.value < 17:
            hit(deck,hand)
            print(hand.__str__()) # pass the hand to be printed
            print('\n Hand Value: ',hand.value)

        if hand.value > 21:
            busts(hand)



def show_some(player,dealer):
    #print(dealer_hand.cards[0])
    print('\n'+ dealer.who +'\'s Hand:\n ?????\n',dealer.cards[0])
    player.adjust_for_ace()
    print(player)
    print('\n player value:',player.value)

def show_all(player,dealer):
    print(dealer_hand)
    print(player_hand)

def busts(hand):
    print(' ' + hand.who + ' Bust\'s')
    hand.busted = True


def winner(player,dealer,chip):
    if player.value  > dealer.value:
        print('Player wins')
        chip.win()
        print('Chips: ',chip.total)
    elif player.value < dealer.value:
        print('Dealer wins')
        chip.lose()
        print('Chips: ',chip.total)
    else:
        push(player,dealer)

def push(player,dealer):
    print('Its a push')
# GAMEPLAY!

print('Welcome to single Deck BlackJack! Get as close to 21 as you can without going over!\nDealer hits until she reaches 17. Aces count as 1 or 11.\nThe Table limit is 100 minimum bet is 20!')

while b_playing:
    #pdb.set_trace()
    #lets create the Deck
    my_chips = Chips() 
 
 

    while my_chips.total > 0 and b_playing:
        my_deck = Deck()
        my_deck.shuffle()

        take_bet(my_chips)

        player_hand = Hand('Player')
        dealer_hand = Hand('Dealer')
       
        #intial hand for dealer
        dealer_hand.add_card(my_deck.deal())
        dealer_hand.add_card(my_deck.deal())
        
        #intial hand for player
        player_hand.add_card(my_deck.deal())
        player_hand.add_card(my_deck.deal())
        
        show_some(player_hand,dealer_hand)
        
        hit_or_stand(my_deck,player_hand)
     
        if player_hand.busted == True:
            show_all(player_hand,dealer_hand)
            print('\nDealer wins: ',dealer_hand.value)
            my_chips.lose()
            print('Chips: ',my_chips.total)
            

        else:
            show_all(player_hand,dealer_hand)
            hit_or_stand(my_deck,dealer_hand)
            if dealer_hand.busted == True:
              print('\nPlayer wins')
              my_chips.win()
              print('Chip: ',my_chips.total)          
            else:
               winner(player_hand,dealer_hand,my_chips)

        if my_chips.total > 0:
            new_game = input("\nWould you like to play another hand? Enter 'y' or 'n' ")
            if new_game[0].upper()=='Y':
                b_playing=True
                continue
            else:  # dont want to play anymore
                print(f'\nYour total chips are: {my_chips.total}, don\'t forget to cash out!')
                print("Thanks for playing!")
                b_playing=False
                continue
        else:
            print("\nYou no longer have any chips, better luck next time!")
            b_playing=False
            continue