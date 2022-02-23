from deck.card_encoding import ENCODED_CARDS
from deck.deck_functions import Deck
from game.game_functions import Player

me = Player("me")
deck = Deck(ENCODED_CARDS)
deck.shuffle()

me.add_cards(deck.deal(5))

x = me.play_cards(me.hand[0], me.hand[1])

print("stop")
