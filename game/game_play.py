from deck.card_encoding import ENCODED_CARDS
from deck.deck_functions import Deck
from game.game_functions import Player, Vezimas

me = Player("me")
deck = Deck(ENCODED_CARDS)

game = Vezimas(deck,4)
game.deal_cards()
game.set_trumps()


print("stop")
