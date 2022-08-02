import os
import random
from abc import ABC, abstractmethod
from typing import List, Any, Optional, Iterable, Tuple
from typing import TYPE_CHECKING

from deck.card_encoding import SUITS
from deck.deck_functions import visualise_set_of_cards, Card

if TYPE_CHECKING:
    from game.game_state import GameState

OptionalCardList = List[Optional[Card]]


class PlayerType(ABC):
    """Abstract class for representation of player with ability to make choices in game"""

    @abstractmethod
    def select_card_to_beat(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Method for selecting a card to beat
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to beat with or None
        """
        raise NotImplemented

    @abstractmethod
    def select_card_to_play(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Method for selecting a card to play
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to play or None
        """
        raise NotImplemented


class HumanInput(PlayerType):
    """Human player for the game that asks for input to play card"""

    def select_card_to_beat(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Selects a card to beat with randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to beat with or None
        """
        return self.card_play_input(
            list_of_cards, player, card_stack, play_no, play_history, allow_pickup
        )

    def select_card_to_play(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Selects a card to play randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to play or None
        """
        return self.card_play_input(
            list_of_cards, player, card_stack, play_no, play_history, allow_pickup
        )

    @staticmethod
    def card_play_input(
        list_of_cards: Iterable[Card],
        player: "Player",
        card_stack: OptionalCardList,
        play_no: int,
        play_history: Optional[List[str]] = None,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Visualises all cards and asks for a card to play
        Args:
            list_of_cards: available cards to play from hand
            player: player whose cards to show
            card_stack: card stack to visualise
            play_no: which card is player currently playing
            play_history: history of moves in the game
            allow_pickup: allow pickup of cards flag

        Returns:
            card selected to play"""

        os.system("cls")
        if play_history:
            print(
                f"""Play history:
        {"".join(play_history)}"""
            )
            print(
                "-----------------------------------------------------------------------------------"
            )

        card_idx = None
        legal_idx_to_choose = [
            idx + 1 for idx, card in enumerate(player.hand) if card in list_of_cards
        ]
        print(
            f"""Player {player.name} to play {play_no}{f"st" if play_no == 1 else "nd"} card
        -----------------------------------------------------------------------------------
        Select 0 to pickup cards, or ID of card to play. Your suit: {SUITS[player.suit]}, next player suit: {SUITS[player.next_player.suit]}
        {visualise_set_of_cards(player.hand)}
        Card stack: {[str(c) for c in card_stack[-3:]]}, total stack {len(card_stack)}
        -----------------------------------------------------------------------------------"""
        )

        while card_idx is None:
            try:
                card_idx = int(input("ID of card to play: "))
                if card_idx not in legal_idx_to_choose + [0 if allow_pickup else None]:
                    raise ValueError

            except ValueError:
                print("Bad last input, Try again")
                card_idx = None

        if card_idx:
            return player.hand[card_idx - 1]
        pass


class RandomBot(PlayerType):
    """Bot player for the game that plays random cards"""

    def select_card_to_beat(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Selects a card to beat with randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to beat with or None
        """

        return random.choice(list_of_cards + [None])

    def select_card_to_play(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Card:
        """Selects a card to play randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to play or None
        """

        if allow_pickup is False:
            return random.choice(list_of_cards)
        return random.choice(list_of_cards + [None])


class AdvancedBot(PlayerType):
    """Bot player for the game that plays cards of maximum value"""

    @staticmethod
    def evaluate_cards(
        list_of_cards: OptionalCardList, player: "Player"
    ) -> Optional[Card]:
        """Evaluates card value
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move

        Returns:
            List of tuple (card, eval)
        """
        if not list_of_cards:
            return None

        player_suit = player.suit
        next_suit = player.next_player.suit
        next_suit_2 = player.next_player.next_player.suit

        ranking = {
            next_suit_2: 10,
            next_suit: 20,
            player_suit: 30,  # overwrites if next_suit_2==current_suit
        }

        card_rankings = [
            (card, ranking.get(card.suit, 0) + card.face) for card in list_of_cards
        ]

        return min(card_rankings, key=lambda x: x[1])[0]

    def select_card_to_beat(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Selects a card to beat with randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to beat with or None
        """

        evaluated_card = self.evaluate_cards(list_of_cards, player)
        trump_cards = len(list(filter(lambda x: x.suit == player.suit, player.hand)))
        trump_in_stack = len(list(filter(lambda x: x.suit == player.suit, card_stack)))
        if not evaluated_card:
            return None

        if (
            len(player.hand) >= 3
            and trump_cards <= 1
            and evaluated_card.suit == player.suit
        ):  # prevent play with no trumps
            return None

        if trump_in_stack >= int(len(card_stack) / 2):  # take good stack
            return None

        return evaluated_card

    def select_card_to_play(
        self,
        list_of_cards: OptionalCardList,
        player: "Player",
        card_stack: OptionalCardList,
        play_history: List[str],
        game_state: "GameState",
        play_no: int,
        allow_pickup: bool = True,
    ) -> Optional[Card]:
        """Selects a card to play randomly
        Args:
            list_of_cards: list of card to chose from
            player: player to make the move
            card_stack: cards on the table
            play_history: history of all moves
            game_state: game state encoding
            play_no: placement of 1st or 2nd card (1,2)
            allow_pickup: flag if card pickup is a viable move

        Returns:
            Card to play or None
        """

        evaluated_cards = self.evaluate_cards(list_of_cards, player)

        # TODO: implement
        pass


class Player:
    """Represents player for the game, containing his name, score and current hand
    Args:
        name: name of the player
        player_type: card input type class
    """

    def __init__(self, name: str, player_type: PlayerType = HumanInput):
        self.name: str = name
        self.player_type: Optional[PlayerType] = player_type

        self.score: int = 0
        self.hand: List[Card] = []

        self.next_player_init: Optional[Player] = None
        self.previous_player_init: Optional[Player] = None
        self.next_player: Optional[Player] = None
        self.previous_player: Optional[Player] = None

        self.suit: Optional[int] = None
        self.starting_player: bool = False

    def add_cards(self, list_of_cards: List[Card]):
        """Method to add cards to the players hand
        Args:
            list_of_cards: list of tuple that represents a card to add to players hand
        """
        self.hand = self.hand + list_of_cards

    def remove_cards(self, list_of_cards: List[Card]):
        """Method to remove cards from the players hand
        Args:
            list_of_cards: list of tuple that represents a card to remove from players hand
        """
        [self.hand.remove(card) for card in list_of_cards if card in self.hand]

    def remove_all_cards(self):
        """Method to remove all cards from the players hand"""
        self.hand = []

    def has_card(self, card: Card):
        """Method to check if a player has specified card in hand
        Args:
            card: tuple that represents a card to check if player has

        Returns:
            Boolean flag if the card is in hand
        """

        return card in self.hand

    # Interesting case of Forward reference https://www.python.org/dev/peps/pep-0484/#forward-references
    def add_player_reference(self, prev_player: "Player", next_player: "Player"):
        """Method to add a reference to a player playing after and before current player
        Args:
            prev_player: previous player in line to play
            next_player: next player in line to play
        """
        self.previous_player_init = prev_player
        self.next_player_init = next_player

        self.previous_player = prev_player
        self.next_player = next_player

    def reset_player_reference(self):
        """Method to reset initial references to a player playing after and before current player
        Args:
        """
        if (self.previous_player_init is None) or (self.next_player_init is None):
            raise AttributeError(f"{self.name} references not initialized")

        self.previous_player = self.previous_player_init
        self.next_player = self.next_player_init

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

    def __len__(self):
        return len([el for el in self.list if el])

    def remove(self, e: Any):
        """Method to remove element from list
        Args:
            e: element to remove from list
        """
        self.list[self.list.index(e)] = None

    def elements(self):
        """Method to return list of elements still in cycle"""
        return [el for el in self.list if el]
