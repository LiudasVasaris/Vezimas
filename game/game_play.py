from deck.card_encoding import ENCODED_CARDS
from deck.deck_functions import Deck
from game.game_functions import Player, Vezimas, VezimasSubgame

if __name__ == '__main__':

    deck = Deck(ENCODED_CARDS)

    game = Vezimas(deck,4)
    game.deal_cards()
    game.set_trumps()
    game.share_nines()

    trick = VezimasSubgame(game)

    trick.start_game()



print("stop")
