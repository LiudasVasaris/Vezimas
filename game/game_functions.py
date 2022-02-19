from typing import Optional, List

from deck.card_encoding import card_type


class Player:
    def __init__(self, name: str):
        self.name = name
        self.score = []
        self.hand = []

    def add_cards(self, list_of_cards: List[card_type]):
        self.hand = self.hand + list_of_cards

    def play_cards(
        self, beat_card: Optional[card_type], play_card: Optional[card_type]
    ) -> List[card_type]:

        cards_to_stack = []

        if beat_card:
            self.hand.remove(beat_card)
            cards_to_stack.append(beat_card)
        if play_card:
            self.hand.remove(play_card)
            cards_to_stack.append(play_card)

        return cards_to_stack


class Vezimas:
    def __init__(self, player_count: int, player_names: Optional[List[str]] = None):
        if player_names and player_count != len(player_names):
            raise ValueError(
                f"Incorrect number of names provided, expected {player_count}, got {len(player_names)}"
            )

        self.player_names = player_names or [
            f"Player {i}" for i in range(1, player_count + 1)
        ]

        self.players = {name: Player(name) for name in self.player_names}
