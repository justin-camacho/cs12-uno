# pyright: strict

from __future__ import annotations
from collections.abc import MutableSequence, Sequence

from kit import Card, Color, Value, Character, Player, Bot
from model import UnoModel
from random import Random
from typing import ClassVar

import sys
import time

class UnoView:
    VAL: ClassVar[dict[str, str]] = {
        '1': 'One',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine',
        '+': 'Plus Two',
        '#': 'Plus Four',
        '←': 'Reverse',
        'Ø': 'Skip',
    }
    COL: ClassVar[dict[str, str]] = {
        '🟥': 'Red',
        '🟧': 'Orange',
        '🟨': 'Yellow',
        '🟩': 'Green',
        '🟦': 'Blue',
        '🟪': 'Purple',
    }
    
    def ask_for_decision(self, deck: MutableSequence[Card], usable: Sequence[Card]) -> int:
        p: int = -3
        cl: int = len(deck)
        valid: Sequence[int] = [idx for idx, card in enumerate(deck) if card in usable]

        while not (p in (-1, -2) or (0 <= p < cl and p in valid)):
            try:
                p = int(input(f'Pick a Valid Card Index {valid}, Draw (-1), or Exit (-2): '))
            except ValueError:
                p = -3
            
        return p
    
    def display_pile_card(self, card: Card, cl: int) -> None:
        print(f'{"PILE":^{cl}}')
        
        for row in str(card).splitlines():
            print(f'{row:^{cl if row and row[3] not in Color else cl-1}}')
        print()
        
    def display_player_card(self, player: Player, cl: int) -> None:
        lay: Sequence[Sequence[str]] = [str(card).splitlines() for card in player.deck]
        out: Sequence[str] = ['   '.join(row) for row in zip(*lay)]
        
        print(f'{"PLAYER'S CARDS":^{cl}}')
        print(*out, sep='\n')
        
    def display_bot_card(self, bot: Bot, cl: int) -> None:
        mystery: str = '''
┍━━━━━━┑
│     ?│
│      │
│  ⬛  │
│      │
│?     │
┕━━━━━━┙
'''
        lay: Sequence[Sequence[str]] = [mystery.splitlines() for _ in bot.deck]
        out: Sequence[str] = ['   '.join(row) for row in zip(*lay)]
        
        print(f'{"BOT'S CARDS":^{cl}}')
        print(*out, sep='\n')
    
    def display_bot_move(self, name: str, value: Value, color: Color) -> None:
        print(f'> {name} played a {self.COL[color]} {self.VAL[value]}!')
        print()
        
    def display_bot_draw(self, name: str) -> None:
        print(f'> {name} drew a card!')
        print()
        
    def display_cards_left(self, characters: Sequence[Character]) -> None:
        
        print('----------')
        print('CARDS LEFT')
        print('----------')
        print()
        for character in characters:
            print(f'{character.__class__.__name__} \'{character.name}\': {len(character.deck)}')
        print()        
          
    def display_stats(self, turn: int, name: str, nxt: str, cl: int) -> None:
        print(f'{f"Turn: {turn+1} <~> Name: {name} <~> Next: {nxt}":^{cl}}')
        print()
        
    def display_interface(self, cl: int) -> None:
        print('<~>'.join([f'{f"  [C{idx}]  ":^8}' for idx in range(cl)]))
        print()
        
    def display_uno_reminder(self, cl: int) -> None:
        print(f'{"---------------------------":^{cl}}')
        print(f'{"PLAYING A CARD REQUIREMENTS":^{cl}}')
        print(f'{"---------------------------":^{cl}}')
        print(f'{"Same Value or Color":^{cl}}')
        print()
        
    def wipe_console(self) -> None:
        for _ in range(100):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
    
class UnoController:
    def __init__(self, model: UnoModel, view: UnoView):
        self._model = model
        self._view = view
    
    def start(self):
        model: UnoModel = self._model
        view: UnoView = self._view 
        
        view.wipe_console()
        model.set_up()
        while not model.is_game_over:
            active: Character = model.characters[model.pointer % len(model.characters)]
            centre: int = 8 * len(active.deck) + 3 * (len(active.deck) - 2)
            
            if isinstance(active, Player):
                top: Card = model.pile[-1]
                nxt: str = model.characters[(model.pointer + (model.weight * model.rotation)) % len(model.characters)].name
                
                view.display_uno_reminder(centre)
                view.display_stats(model.turn, active.name, nxt, centre)
                view.display_pile_card(model.pile[-1], centre)
                view.display_player_card(active, centre)
                view.display_interface(len(active.deck))
                view.display_cards_left(model.characters)
                
                decision: int = view.ask_for_decision(active.deck, active.usable(top.value, top.color))
                
                if 0 <= decision < len(active.deck):
                    model.add_to_pile(active.use(active.deck[decision]))
                    model.analyze_top()
                elif decision == -1:
                    active.draw(model.DECK)
                elif decision == -2:
                    view.wipe_console()
                    sys.exit()
                else:
                    raise ValueError
                
                view.wipe_console()
                
            elif isinstance(active, Bot):
                top: Card = model.pile[-1]
                nxt: str = model.characters[(model.pointer + (model.weight * model.rotation)) % len(model.characters)].name
                
                view.display_stats(model.turn, active.name, nxt, centre)
                view.display_pile_card(top, centre)
                view.display_bot_card(active, centre)
                view.display_interface(len(active.deck))
                view.display_cards_left(model.characters)
                
                try:
                    select: Card = active.use(model.rng.choice(active.usable(top.value, top.color)))
                    
                    model.add_to_pile(select)
                    model.analyze_top()
                    
                    time.sleep(2 * (1 + Random().random()))
                    
                    view.wipe_console()
                    view.display_bot_move(active.name, select.value, select.color)
                except IndexError:
                    active.draw(model.DECK)
                    
                    time.sleep(2 * (1 + Random().random()))
                    
                    view.wipe_console()
                    view.display_bot_draw(active.name)
            
            model.advance_turn()
                
if __name__ == '__main__':
    print('Welcome to Uno!')
    print('(Assumption: you know the rules of the game)')
    print()
    
    number: int = -1
    seed: int = 0
    player: str = ''
    names: MutableSequence[str] = []
    
    while not 0 < number <= 5:
        try:
            number = int(input("Enter number of Bots (0, 5]: "))
        except ValueError:
            pass
        
    while not player:
        player = input("Enter Player name: ")
        
    for idx in range(number):
        while not (name := input(f"Enter Bot {idx+1} name: ")):
            pass
        else:
            names.append(name)
            
    while True:
        try:
            seed = int(input("Enter seed: "))
        except ValueError:
            pass
        else:
            break
    
    game: UnoController = UnoController(UnoModel([Player(player), *(Bot(name) for name in names)], Random(seed)), UnoView())
    game.start()