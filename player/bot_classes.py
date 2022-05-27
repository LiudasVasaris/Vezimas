import random
from abc import ABC, abstractmethod
from typing import List

from deck.deck_functions import Card


class BaseBotClass(ABC):
    @abstractmethod
    def select_card_to_beat(self, list_of_cards: List[Card]) -> Card:
        """Method for selecting a card to beat
        Args:
            list_of_cards: list of card to chose from

        Returns:
            Card to beat with
        """
        raise NotImplemented

    @abstractmethod
    def select_card_to_play(self, list_of_cards: List[Card]) -> Card:
        """Method for selecting a card to play
        Args:
            list_of_cards: list of card to chose from

        Returns:
            Card to play
        """
        raise NotImplemented


class RandomBot(BaseBotClass):
    """Bot player for the game that plays random cards"""

    def select_card_to_beat(self, list_of_cards: List[Card]) -> Card:
        """Selects a card to beat with randomly
        Args:
            list_of_cards: list of card to chose from

        Returns:
            Card to beat with
        """
        return random.choice(list_of_cards)

    def select_card_to_play(self, list_of_cards: List[Card]) -> Card:
        """Selects a card to play randomly
        Args:
            list_of_cards: list of card to chose from

        Returns:
            Card to play
        """
        return random.choice(list_of_cards)
