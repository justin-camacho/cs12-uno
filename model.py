# pyright: strict

from collections.abc import MutableSequence, Sequence

from kit import Card, Character, Color, Value, Rotation
from random import Random
from typing import ClassVar

class UnoModel:
    DECK: ClassVar[MutableSequence[Card]] = [Card(value, color) for value in Value for color in Color]
    
    def __init__(self, characters: Sequence[Character], rng: Random):
        self._characters: Sequence[Character] = characters
        self._turn: int = 0
        self._rng: Random = rng
        self._pile: MutableSequence[Card] = []
        self._rotation: Rotation = Rotation.CLOCKWISE
        self._pointer: int = 0
        self._weight: int = 1
        
    @property
    def characters(self) -> Sequence[Character]:
        return self._characters
    
    @property
    def turn(self) -> int:
        return self._turn
    
    @property
    def rng(self) -> Random:
        return self._rng
    
    @property
    def pile(self) -> MutableSequence[Card]:
        return self._pile
    
    @property
    def rotation(self) -> Rotation:
        return self._rotation
    
    @property
    def pointer(self) -> int:
        return self._pointer
    
    @property
    def weight(self) -> int:
        return self._weight
    
    @property
    def is_game_over(self) -> bool:
        return any([not len(player.deck) for player in self._characters])
    
    def add_to_pile(self, card: Card) -> None:
        self._pile.append(card)
    
    def plustwo(self) -> None:
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._weight = 2
        
    def plusfour(self) -> None:
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._characters[(self._pointer + (self._weight * self._rotation)) % len(self._characters)].draw(self.DECK)
        self._weight = 2
        
    def reverse(self) -> None:
        self._rotation = Rotation.COUNTERCLOCKWISE if self._rotation == Rotation.CLOCKWISE else Rotation.CLOCKWISE
        
    def skip(self) -> None:
        self._weight = 2
        
    def get_random_decision(self, idx: int) -> None:
        top: Card = self._pile[-1]
        dec: Sequence[Card] = self._characters[idx].usable(top.value, top.color)
        
        try:
            self.add_to_pile(self._rng.choice(dec))
        except IndexError:
            self._characters[idx].draw(self.DECK)
            
    def analyze_top(self) -> None:
        top: Card = self._pile[-1]
        
        match top.value:
            case Value.PLUS:
                self.plustwo()
            case Value.PLUSFOUR:
                self.plusfour()
            case Value.REVERSE:
                self.reverse()
            case Value.SKIP:
                self.skip()
            case _:
                pass
    
    def set_up(self) -> None:
        self._rng.shuffle(self.DECK)
        
        for _ in range(7):
            for player in self._characters:
                player.draw(self.DECK)
                
        self.add_to_pile(self.DECK.pop())
    
    def advance_turn(self) -> None:
        
        self._pointer += (self._weight * self._rotation)
        self._weight = 1
        self._turn += 1