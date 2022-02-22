from typing import Optional, List

from deck.card_encoding import card_type, QUEEN_OF_SPADES, SUITS
from deck.deck_functions import Deck
from itertools import cycle


class Player:
    """Represents player for the game, containing his name, score and current hand
    Args:
        name: name of the player
    """

    def __init__(self, name: str):
        self.name: str = name

        self.score: List[str] = []
        self.hand: List[card_type] = []
        self.next_player: Optional[Player] = None
        self.suit: Optional[int]

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

    # Interesting case of Forward reference https://www.python.org/dev/peps/pep-0484/#forward-references
    def add_next_player(self, player: "Player"):
        self.next_player = player


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

        self.players = [Player(name) for name in self.player_names]

        # removes first element and adds it back again, essentially rotating list by one element
        shifted_players_list = self.players.copy()
        shifted_players_list.append(shifted_players_list.pop(0))

        _ = [
            player.add_next_player(next_player)
            for player, next_player in zip(self.players, shifted_players_list)
        ]

    def deal_cards(self):
        """Method that shuffles and deals cards to the players"""
        cards_per_player = int(len(self.deck) / len(self.players))
        self.deck.shuffle()
        for player in self.players:
            player.add_cards(self.deck.deal(cards_per_player))

    def set_trumps(self):
        """Setting trumps for the players using Queen of spades start of game method"""
        for player in self.players:
            if player.has_card(QUEEN_OF_SPADES):
                player.suit = SUITS.keys()[0]  # First suit is spades

                for set_suit in SUITS.keys()[1:]:
                    player.next_player.suit = set_suit
