from typing import List, Any, Optional

from deck.card_encoding import SUITS
from deck.deck_functions import visualise_set_of_cards, Card


class Player:
    """Represents player for the game, containing his name, score and current hand
    Args:
        name: name of the player
    """

    def __init__(self, name: str):
        self.name: str = name

        self.score: int = 0
        self.hand: List[Card] = []
        self.next_player: Optional[Player] = None
        self.suit: Optional[int] = None
        self.starting_player: bool = False

    def add_cards(self, list_of_cards: List[Card]):
        """Method to add cards to the players hand
        Args:
            list_of_cards: list of tuple that represents a card to add to players hand
        """
        self.hand = self.hand + list_of_cards

    def remove_cards(self, list_of_cards: List[Card]):
        """Method to remove cards to the players hand
        Args:
            list_of_cards: list of tuple that represents a card to remove from players hand
        """
        [self.hand.remove(card) for card in list_of_cards if card in self.hand]

    def has_card(self, card: Card):
        """Method to check if a player has specified card in hand
        Args:
            card: tuple that represents a card to check if player has

        Returns:
            Boolean flag if the card is in hand
        """

        return card in self.hand

    # Interesting case of Forward reference https://www.python.org/dev/peps/pep-0484/#forward-references
    def add_next_player(self, player: "Player"):
        """Method to add a reference to a player playing after current player
        Args:
            player: Next player in line to play
        """
        self.next_player = player

    def sort_cards(self):
        """Method for sorting player cards"""
        self.hand = sorted(self.hand, key=lambda card: (card.suit, card.face))


class MyCycle:
    """Object that allows to cycle over given list and remove elements from it"""

    def __init__(self, lst: List[Optional[Player]]):
        self.list = lst

    def __iter__(self):
        while True:
            items_left = False
            for x in self.list:
                if x is not None:
                    items_left = True
                    yield x
            if not items_left:
                return

    def remove(self, e: Any):
        """Method to remove element from list
        Args:
            e: element to remove from list
        """
        self.list[self.list.index(e)] = None


def card_play_input(player: Player, card_stack: List[Card]) -> Card:
    """Visualises all cards and asks for a card to play
    Args:
        player: player whose cards to show
        card_stack: card stack to visualise

    Returns:
        card selected to play"""

    print("-----------------------------------------------------------------------")
    print(
        f"Select 0 to pickup cards, or ID of card to play. Your suit: {SUITS[player.suit]}"
    )
    print(visualise_set_of_cards(player.hand))
    print(
        f"Card stack: {[str(c) for c in card_stack[-3:]]}, total stack {len(card_stack)}"
    )
    print("-----------------------------------------------------------------------")

    card_idx = None

    while card_idx is None:
        try:
            card_idx = int(input("ID of card to play: "))
            if card_idx not in list(range(len(player.hand) + 1)):
                raise ValueError("Incorrect ID of card")
        except ValueError:
            card_idx = None
            print("Bad last input, Try again")

    if card_idx:
        return player.hand[card_idx - 1]
    pass
