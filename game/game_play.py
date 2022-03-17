from deck.card_encoding import ENCODED_CARDS
from deck.deck_functions import Deck
from game.game_functions import Player, Vezimas, VezimasSubgame

me = Player("me")
deck = Deck(ENCODED_CARDS)

game = Vezimas(deck,4)
game.deal_cards()
game.set_trumps()
game.share_nines()

trick = VezimasSubgame(game)

for player in trick.player_cycle:
    trick.card_play_input(player)


print("stop")
