from deck.deck_functions import Deck, ENCODED_CARDS
from game.game_functions import Vezimas, VezimasSubgame

if __name__ == "__main__":

    deck = Deck(ENCODED_CARDS)

    game = Vezimas(deck, 4)
    game.deal_cards()
    game.set_trumps()
    game.share_nines()
    game.sort_cards()

    trick = VezimasSubgame(game)

    trick.start_game()


print("stop")
