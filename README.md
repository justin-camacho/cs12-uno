# cs12-uno
Sample Uno game program, with unit tests, made as practice for CS12. Made by Justin Camacho.


### Object of the Game 🏆
[(source)](https://www.unorules.com/)

**Uno** is the highly popular card game played by millions around the globe. This game is played by matching and then 
discarding the cards in one’s hand till none are left.

To prevent the player with the first turn from gaining an advantage, the card on top of the draw pile will be 
**revealed** and play according to that card.

### Rules of the Game 📜
[(source)](https://www.unorules.com/)

You have to match either by the **number**, **color**, or the **action**.

If the player has no matches or they choose not to play any of their cards even though they might have a match, 
they must **draw** a card from the **draw** pile.

For the sake of this program, even if the drawn card can be played on the same turn, it must be **kept** until
the player's **next turn**. All action cards revealed before the start of the game will also have **no effect**.
No **'UNO!'** calls will also be implemented.

The first person with no cards remaining is the **winner**.

### Program Mechanics 🛠️

The player will be prompted to enter some number of **bots** (`(0, 5]`), everyone's **names**, and a **seed**.
Play will begin from there and continue until either:

1. Some character has no cards remaining in their hand
2. The player **exits** the game

### Running the Game 🎮
```bash
python3 uno.py
```

### Running Pytest 🎬
```bash
coverage run --branch -m pytest && coverage html
```

Alternative Command:

```bash
python3 -m coverage run --branch -m pytest && python3 -m coverage html
```

### Farthest Phase 🥉
> **Phase 3**.

(There are no phases)