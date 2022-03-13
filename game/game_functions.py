from typing import Optional, List, Any

from deck.card_encoding import card_type, QUEEN_OF_SPADES, SUITS, NINES
from deck.deck_functions import Deck, visualise_set_of_cards
from itertools import cycle


class MyCycle:
    """Object that allows to cycle over given list and remove elements from it"""

    def __init__(self, lst: List[Any]):
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
        self.suit: Optional[int] = None
        self.starting_player: bool = False

    def add_cards(self, list_of_cards: List[card_type]):
        """Method to add cards to the players hand
        Args:
            list_of_cards: list of tuple that represents a card to add to players hand
        """
        self.hand = self.hand + list_of_cards

    def remove_cards(self, list_of_cards: List[card_type]):
        """Method to remove cards to the players hand
        Args:
            list_of_cards: list of tuple that represents a card to remove from players hand
        """
        [self.hand.remove(card) for card in list_of_cards if card in self.hand]

    def play_cards(
        self, beat_card: Optional[card_type], play_card: Optional[card_type]
    ) -> List[card_type]:
        """Method to play cards from players hand
        Args:
            beat_card: tuple that represents a card placed to beat the top card
            play_card: tuple that represents a card placed to play after beating

        Returns:
            List of cards to be played"""

        cards_to_stack = []

        if beat_card:
            self.hand.remove(beat_card)
            cards_to_stack.append(beat_card)
        if play_card:
            self.hand.remove(play_card)
            cards_to_stack.append(play_card)

        return cards_to_stack

    def has_card(self, card: card_type):
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
            nine_to_add = (9, player.suit)
            player.add_cards([nine_to_add])

    def remove_starting_player_flags(self):
        """Method for resetting starting player flag"""
        for player in self.players:
            player.starting_player = False

    def get_starting_player(self):
        """Method for retrieving starting player"""
        for player in self.players:
            if player.starting_player:
                return player
        raise ValueError("Starting player not set")


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

    # TODO: where should this go
    @staticmethod
    def card_play_input(player: Player) -> card_type:
        """Visualises all cards and asks for a card to play
        Args:
            player: player whose cards to show

        Returns:
            card selected to play"""
        visualise_set_of_cards(player.hand)
        card_idx = None

        while card_idx is None:
            try:
                card_idx = int(input("ID of card to play: "))
                if card_idx not in range(len(player.hand)):
                    raise ValueError("Incorrect ID of card")
            except ValueError:
                print("Try again")

        return player.hand[card_idx]
    
