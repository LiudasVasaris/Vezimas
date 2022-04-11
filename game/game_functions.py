import os
from typing import Optional, List

from deck.card_encoding import SUITS
from deck.deck_functions import Deck, Card, QUEEN_OF_SPADES, NINES
from player.player_functions import Player, MyCycle, card_play_input


class Vezimas:
    """Represents the class used to play the game Vezimas
    Args:
        deck_of_cards: deck to be used for the game
        player_count: number of players that will start the game
        player_names: (Optional) provide names for players, otherwise they will be numbered"""

    def __init__(
        self,
        deck_of_cards: Deck,
        player_count: int,
        player_names: Optional[List[str]] = None,
    ):
        self.deck = deck_of_cards
        self.player_count = player_count

        if player_names and player_count != len(player_names):
            raise ValueError(
                f"Incorrect number of names provided, expected {player_count}, got {len(player_names)}"
            )

        self.player_names = player_names or [
            f"Player {i}" for i in range(0, player_count)
        ]

        self.players = [Player(name) for name in self.player_names]

        # removes first element and adds it back again, essentially rotating list by one element
        shifted_players_list = self.players.copy()
        shifted_players_list.append(shifted_players_list.pop(0))

        [
            player.add_next_player(next_player)
            for player, next_player in zip(self.players, shifted_players_list)
        ]

    def deal_cards(self):
        """Method that shuffles and deals cards to the players"""
        cards_per_player = int(len(self.deck) / self.player_count)
        self.deck.shuffle()
        for player in self.players:
            player.add_cards(self.deck.deal(cards_per_player))

    def set_trumps(self):
        """Setting trumps for the players using Queen of spades start of game method

        Returns:
            Player who got the Queen of spades (to start off the first game)"""
        suit_list = list(SUITS.keys())
        for player in self.players:
            if player.has_card(QUEEN_OF_SPADES):
                player.suit = suit_list[0]  # First suit is spades
                player.starting_player = True  #  Queen of spades starts game
                next_player = player.next_player

                for set_suit in suit_list[1:]:
                    if next_player.suit:
                        break
                    next_player.suit = set_suit
                    next_player = next_player.next_player
                return player

    def share_nines(self):
        """Method for `returning` each nine card to its suits owner"""
        for player in self.players:
            player.remove_cards(NINES)
            nine_to_add = Card((9, player.suit))
            player.add_cards([nine_to_add])

    def remove_starting_player_flags(self):
        """Method for resetting starting player flag"""
        for player in self.players:
            player.starting_player = False

    def get_starting_player(self) -> Player:
        """Method for retrieving starting player"""
        for player in self.players:
            if player.starting_player:
                return player
        raise ValueError("Starting player not set")

    def sort_cards(self):
        """Method for sorting cards of each player"""
        [player.sort_cards() for player in self.players]

    def check_worst_player(self) -> Player:
        """Method for checking score of worst player"""
        return max(self.players, key=lambda p: p.score)

    def reset_cards(self):
        """Method for resetting deck and player hands after the trick"""
        self.deck = self.deck.reset_deck()
        [player.remove_all_cards() for player in self.players]


def check_play_validity(
    card_stack: List[Card], card_to_beat: Optional[Card], player: Player
) -> bool:
    """Checks if played card obeys the game rules
    Args:
        card_stack: stack of cards already played
        card_to_beat: card played to beat the stack
        player: player that is making the play

    Returns: True if play is correct (or no card provided), False otherwise
    """
    if not card_to_beat:
        return True
    last_card = card_stack[-1]
    next_player_suit = None
    next_player_to_play = player.next_player

    while next_player_suit is None:
        if next_player_to_play.hand:
            next_player_suit = next_player_to_play.suit
        else:
            next_player_to_play = next_player_to_play.next_player

    if last_card.suit == player.suit and card_to_beat.suit != player.suit:
        print("Card suit is incorrect")
        return False

    if last_card.suit == player.suit and last_card > card_to_beat:
        print("Card face value too low")
        return False

    if last_card.suit == next_player_suit and card_to_beat.suit != player.suit:
        print("Card suit is incorrect")
        return False

    if last_card.suit != next_player_suit and last_card.suit != player.suit:
        if card_to_beat.suit != player.suit:
            if card_to_beat.suit != last_card.suit:
                print("Card suit is incorrect")
                return False
            if last_card > card_to_beat:
                print("Card face value too low")
                return False

    return True


class VezimasSubgame:
    """Class of playing the trick/subgame of Vezimas"""

    def __init__(self, main_game: Vezimas):
        self.main_game = main_game

        # creates cycle list starting from player who has its starting player flag set
        _player_to_add = self.main_game.get_starting_player()
        _player_list = []
        for i in range(self.main_game.player_count):
            _player_list.append(_player_to_add)
            _player_to_add = _player_to_add.next_player

        self.player_cycle = MyCycle(_player_list)
        self.card_stack = []

    def pickup_cards(self, player: Player):
        """Method for picking up cards and resetting card stack"""
        player.add_cards(self.card_stack)
        self.card_stack = []

    def start_game(self):
        """Method for starting the trick of Vezimas"""

        for player_turn in self.player_cycle:
            os.system("cls")
            print(f"{player_turn.name} select card(s) to play:")

            # If card stack is empty play one card
            if not self.card_stack:
                while True:
                    card_to_play_first = card_play_input(player_turn, self.card_stack)
                    if card_to_play_first:
                        break
                    print("Cannot pick up empty stack")

                player_turn.remove_cards([card_to_play_first])
                self.card_stack.append(card_to_play_first)

            # If card stack is not empty play cards
            else:

                while True:
                    card_to_beat = card_play_input(player_turn, self.card_stack)
                    if check_play_validity(self.card_stack, card_to_beat, player_turn):
                        break

                while True:  # To allow premature end of code

                    if not card_to_beat:
                        # Pickup cards, end turn
                        self.pickup_cards(player_turn)
                        break
                    player_turn.remove_cards([card_to_beat])
                    self.card_stack.append(card_to_beat)

                    if len(player_turn.hand) == 0:
                        # If no cards in hand, end turn
                        break

                    card_to_play = card_play_input(player_turn, self.card_stack)
                    if not card_to_play:
                        # Pickup cards, end turn
                        self.pickup_cards(player_turn)
                        break
                    player_turn.remove_cards([card_to_play])
                    self.card_stack.append(card_to_play)

            # Remove player from playing trick if he has no more cards
            if not player_turn.hand:
                self.player_cycle.remove(player_turn)
                print(f"{player_turn.name} won")

            # End game when there is only one person left
            if len(self.player_cycle.list) == 1:
                self.main_game.players[player_turn.name].score += 1
                print(f"{player_turn.name} lost the game")
                return player_turn

            if len(self.player_cycle.list) == 0:
                print(f"Game was tied")
                break
