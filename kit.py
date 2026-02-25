# pyright: strict

from collections.abc import MutableSequence, Sequence

from enum import IntEnum, StrEnum

class Value(StrEnum):
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    PLUS = '+'
    PLUSFOUR = '#'
    REVERSE = '←'
    SKIP = 'Ø'


class Color(StrEnum):
    RED = '🟥'
    ORANGE = '🟧'
    YELLOW = '🟨'
    GREEN = '🟩'
    BLUE = '🟦'
    PURPLE = '🟪'
    
    
class Rotation(IntEnum):
    CLOCKWISE = 1
    COUNTERCLOCKWISE = -1

class Card:
    def __init__(self, value: Value, color: Color):
        self._value: Value = value
        self._color: Color = color
    
    def __str__(self):
        return f"""
┍━━━━━━┑
│     {self._value}│
│      │
│  {self._color}  │
│      │
│{self._value}     │
┕━━━━━━┙
"""
   
    @property
    def value(self) -> Value:
        return self._value
    
    @property
    def color(self) -> Color:
        return self._color

class Character:
    def __init__(self, name: str):
        self._name: str = name
        self._deck: MutableSequence[Card] = []
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def deck(self) -> MutableSequence[Card]:
        return self._deck
        
    def draw(self, cards: MutableSequence[Card]) -> None:
        self._deck.append(cards.pop())
    
    def use(self, choice: Card) -> Card:
        
        for card in self._deck:
            if card is choice:
                self._deck.remove(card)
                return card
            
        raise ValueError
        
    def usable(self, value: Value, color: Color) -> Sequence[Card]:
        return [card for card in self._deck if card.value == value or card.color == color]

class Player(Character):
    pass
    
class Bot(Character):
    pass