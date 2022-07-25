from deck.card_encoding import SUITS
from deck.deck_functions import Deck, ENCODED_CARDS
from game.game_functions import Vezimas, VezimasSubgame
from player.player_functions import RandomBot


def start_game(player_count=4, bot_count=3):
    deck = Deck(ENCODED_CARDS)
    bot_level = RandomBot()
    game = Vezimas(
        deck_of_cards=deck,
        player_count=player_count,
        bot_count=bot_count,
        bot_level=bot_level,
    )
    game.set_player_reference()
    game.deal_cards()
    game.set_trumps()

    while (game_no := game.check_worst_player().score) < 7:
        print(f"Starting game {sum([p.score for p in  game.players])}")
        game.deal_cards()
        game.share_nines()
        game.sort_cards()
        trick = VezimasSubgame(game)
        lost_player = trick.start_game()

        if not lost_player:
            game.remove_starting_player_flags()  # Keep same starting position

        game.reset_player_reference()
        game.reset_cards()

    print(
        {f"{player.name} {SUITS[player.suit]}": player.score for player in game.players}
    )


if __name__ == "__main__":
    start_game(player_count=4, bot_count=4)

print("stop")
