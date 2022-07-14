from typing import List

from deck.deck_functions import Card
from player.player_functions import Player, OptionalCardList


class GameState:
    """Game state representation class, containing adjustment functions and array output
    Args:
        players: players in a given game
    """

    def __init__(
        self, players: List[Player], card_stack: OptionalCardList, card_to_beat: bool
    ):
        self.players = players
        self.player_state = {
            player.name: {
                "is_active": True,
                "suit": player.suit,
                "no_cards": len(player.hand),
                "known_cards": [Card((9, player.suit))],
            }
            for player in players
        }
        self.play_state = {"card_stack": card_stack, "card_to_beat": card_to_beat}

    def add_known_cards(self, list_of_cards: List[Card], player: Player):
        """Marks cards as known in player hands"""
        self.player_state[player.name]["known_cards"] += list_of_cards
        self.player_state[player.name]["no_cards"] += len(list_of_cards)

    def remove_known_cards(self, list_of_cards: List[Card], player: Player):
        """Removes card as known in player hands"""
        [
            self.player_state[player.name]["known_cards"].remove(card)
            for card in list_of_cards
        ]
        self.player_state[player.name]["no_cards"] -= len(list_of_cards)

    def __repr__(self):
        return f"player state: {self.player_state}\nplay state{self.play_state}"
