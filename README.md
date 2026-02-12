# Marble Solitaire

A Python implementation of the classic marble solitaire (peg solitaire) board game with encoding/decoding capabilities for board state representation.

## Game Overview

Marble solitaire is a single-player strategy game played on a cross-shaped board with pegs (marbles). The objective is to remove all but one peg from the board by jumping pegs over adjacent pegs into empty spaces.

### Rules

1. **Starting Position** : The board begins fully populated with pegs except for one empty space in the centre
2. **Valid Moves** : A peg can jump over an adjacent peg into an empty space (horizontally or vertically only, no diagonal moves)
3. **Peg Removal** : When a peg is jumped over, it is removed from the board
4. **Winning Condition** : The game is won when only one peg remains on the board
5. **Losing Condition** : The game is lost when no valid moves remain but multiple pegs are still on the board

### Board Layout

The standard board is a 7×7 grid with a cross shape:

```
    O O O
    O O O
O O O O O O O
O O O . O O O    (. represents the empty starting space)
O O O O O O O
    O O O
    O O O
```

## Interactive Play

The `play()` function provides an interactive command-line interface for playing the game:

```python
# Start an interactive game
game = table()
play(game)
```

The interface will:

1. Display the current board state
2. Show all available moves with numeric IDs
3. Prompt you to select a move by entering its number
4. Execute the move and repeat

## Program Structure

### Classes

#### `cell`

Represents a single position on the game board.

**Attributes:**

* `x` (int): X-coordinate position
* `y` (int): Y-coordinate position
* `mode` (int): Cell state
  * `-1`: Invalid space (outside the cross shape)
  * `0`: Empty space
  * `1`: Occupied space (contains a peg)

**Methods:**

* `getMode()`: Returns the current state of the cell
* `getPos()`: Returns a tuple `(x, y)` of the cell's position
* `changeMode(newMode)`: Updates the cell's state
* `validCell()`: Returns `True` if the cell is a valid playable space

#### `table`

Represents the game board and handles all game logic.

**Attributes:**

* `width`: Board width (default: 7)
* `height`: Board height (default: 7)
* `grid`: 2D list of `cell` objects representing the board
* `invertDirMap`: Dictionary mapping directions to their opposites
* `encodeList`: Character set used for encoding the board state

##### Board Setup

* `createTable()`: Creates an empty 7×7 grid
* `applyTable(mode)`: Initialises the board
  * `mode="play"`: Standard starting position
  * `mode="debug"`: Each cell numbered sequentially for testing

## Encoding System

The program uses a custom base-3 encoding system to represent board states efficiently.

### How it Works

1. **Cell Mode Mapping** :

   - Each cell mode is mapped to a ternary digit:
   - `-1` → `1`
   - `0` → `2`
   - `1` → `3`
2. **Segmentation** :

   - The 49 cells (7×7 board) are divided into segments
   - Segment size is calculated based on the available character set (52 characters)
   - For 52 characters: `segmentSize = floor(log₃(52)) = 3`
   - Each segment encodes 3 cells into a single character
3. **Encoding Format** :

   - `width-height-segmentSize-encodedString`
   - Example: `7-7-3-jhansqwnnxqembsha`

### Example Usage

```python
# Create and set up a game board
game = table()

# Display the current board
game.displayTable()

# Get all valid moves
moves = game.validMoves()
print(f"Available moves: {len(moves)}")

# Make a move (from position 3,5 moving north)
success = game.makeMove(3, 5, "north")

# Encode the current state
encoded = game.encodeGrid()
print(f"Encoded state: {encoded}")

# Check if the game is won
if game.hasWon():
    print("Congratulations! You've won!")
```

## Requirements

* Python 3.8+
* Standard library only (no external dependencies)

## Technical Details

### Coordinate System

* Origin `(0, 0)` is at the top-left corner
* X-axis increases from left to right
* Y-axis increases from top to bottom

### Direction System

Moves are specified using cardinal directions:

* `"north"`: Move upward (decrease Y)
* `"south"`: Move downward (increase Y)
* `"east"`: Move right (increase X)
* `"west"`: Move left (decrease X)

### Move Validation

A move is valid only if:

1. The starting position contains a peg (mode = 1)
2. The adjacent position in the move direction contains a peg (mode = 1)
3. The landing position (two spaces away) is empty (mode = 0)
4. All three positions are within the valid playing area

## Future Enhancements

Future plans include:

* GUI implementation using tkinter, pygame, or pyqt6
* Save/load game states
* Solver algorithm to find winning solutions
* Multiple board size support
