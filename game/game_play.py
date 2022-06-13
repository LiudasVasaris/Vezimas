from deck.deck_functions import Deck, ENCODED_CARDS
from game.game_functions import Vezimas, VezimasSubgame
from player.player_functions import RandomBot


def start_game():
    deck = Deck(ENCODED_CARDS)
    bot_level = RandomBot()
    game = Vezimas(deck_of_cards=deck, player_count=4, bot_count=4, bot_level=bot_level)
    game.set_player_reference()
    game.deal_cards()
    game.set_trumps()

    while game.check_worst_player().score < 7:
        game.share_nines()
        game.sort_cards()
        trick = VezimasSubgame(game)
        lost_player = trick.start_game()

        if not lost_player:
            game.remove_starting_player_flags()  # Keep same starting position

        game.reset_cards()


if __name__ == "__main__":
    start_game()

print("stop")
