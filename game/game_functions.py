from typing import Optional, List

from deck.card_encoding import card_type
from deck.deck_functions import Deck


class Player:
    """Represents player for the game, containing his name, score and current hand
    Args:
        name: name of the player
    """

    def __init__(self, name: str):
        self.name = name
        self.score = []
        self.hand = []

    def add_cards(self, list_of_cards: List[card_type]):
        """Method to add cards to the players hand"""
        self.hand = self.hand + list_of_cards

    def play_cards(
        self, beat_card: Optional[card_type], play_card: Optional[card_type]
    ) -> List[card_type]:
        """Method to play cards from players hand"""

        cards_to_stack = []

        if beat_card:
            self.hand.remove(beat_card)
            cards_to_stack.append(beat_card)
        if play_card:
            self.hand.remove(play_card)
            cards_to_stack.append(play_card)

        return cards_to_stack

    def has_card(self, card: card_type):
        return card in self.hand


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
        if player_names and player_count != len(player_names):
            raise ValueError(
                f"Incorrect number of names provided, expected {player_count}, got {len(player_names)}"
            )

        self.player_names = player_names or [
            f"Player {i}" for i in range(1, player_count + 1)
        ]

        self.players = {name: Player(name) for name in self.player_names}

    def deal_cards(self):
        cards_per_player = int(len(self.deck) / len(self.players))
        for name, player in self.players.items():
            player.add_cards(self.deck.deal(cards_per_player))

    def set_trumps(self):
        pass
