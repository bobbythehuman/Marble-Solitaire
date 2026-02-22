import math
from copy import deepcopy
from time import time
from typing import Union
import numpy as np
from collections import defaultdict
import random


class cell:
    def __init__(self, x: int, y: int, mode: int = -1) -> None:
        self.x = x
        self.y = y
        self.mode = mode

    def getMode(self) -> int:
        """Returns the mode of the cell, -1 for invalid space, 0 for empty space, 1 for occupied space"""
        return self.mode

    def getPos(self) -> tuple[int, int]:
        """Returns the x and y position of the cell as a tuple"""
        return (self.x, self.y)

    def changeMode(self, newMode: int) -> None:
        """Mode is -1 for invalid space, 0 for empty space, 1 for occupied space"""
        self.mode = newMode

    def validCell(self) -> bool:
        """A valid cell is one that is on the board and not an invalid space"""
        if self.mode < 0:
            return False
        x, y = self.getPos()
        if x < 0:
            return False
        if y < 0:
            return False

        return True


class table:
    def __init__(self):
        # -1 = not a valid space
        # 0 = empty space
        # 1 = occupied space
        # left to right for each row
        self.width = 7
        self.height = 7
        self.emptyCells = []
        self.grid: list[list[cell]] = self.createTable()
        self.applyTable("play")
        # self.applyTable("debug")
        self.invertDirMap = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
        }

        self.encodeList = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "!",
            "£",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "=",
            "+",
            "[",
            "]",
            "{",
            "}",
            ";",
            ":",
            "@",
            "#",
        ]
        self.encodeDict = {v: k for k, v in enumerate(self.encodeList)}
        # Pre-calculate segment size to avoid recalculating
        self.BASE = 3
        self.segmentSize = int(math.log(len(self.encodeList)) // math.log(self.BASE))

    def fetchTable(self):
        return self.grid

    def changeCellMode(self, xAxis, yAxis, mode):
        """Changes the mode of the cell at the given coordinates"""
        cellVar: cell = self.grid[yAxis][xAxis]
        cellVar.changeMode(mode)
        if mode == 0:
            self.emptyCells.append(cellVar)
        elif mode == 1:
            if cellVar in self.emptyCells:
                self.emptyCells.remove(cellVar)

    def changeCellModeByCell(self, cellVar: cell, mode):
        """Changes the mode of the given cell"""
        cellVar.changeMode(mode)
        if mode == 0:
            self.emptyCells.append(cellVar)
        elif mode == 1:
            if cellVar in self.emptyCells:
                self.emptyCells.remove(cellVar)

    def createTable(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(cell(x, y))
            grid.append(row)
        # grid = np.array(grid)
        return grid

    def applyTable(self, mode="play"):
        self.emptyCells = []
        if mode == "play":
            for y, row in enumerate(self.grid):
                for x, cellVar in enumerate(row):
                    if y in [0, 1, 5, 6]:
                        if x in [2, 3, 4]:
                            self.changeCellModeByCell(cellVar, 1)
                    elif y in [2, 3, 4]:
                        self.changeCellModeByCell(cellVar, 1)
            self.changeCellMode(3, 3, 0)

        elif mode == "debug":
            increment = 1
            for y, row in enumerate(self.grid):
                for x, cellVar in enumerate(row):
                    if y in [0, 1, 5, 6]:
                        if x in [2, 3, 4]:
                            self.changeCellModeByCell(cellVar, increment)
                            increment += 1
                    elif y in [2, 3, 4]:
                        self.changeCellModeByCell(cellVar, increment)
                        increment += 1
            self.changeCellMode(3, 3, 0)

    def displayTable(self):
        for row in self.grid:
            stringVar = ""
            for cellVar in row:
                stringVar += f"\t{cellVar.getMode()}"
            print(stringVar)
        print("\n")

    def fetchCellContent(self, content=1, valRange=False) -> list[cell]:
        foundCells = []
        if self.emptyCells and content == 0 and not valRange:
            return self.emptyCells
        for y, row in enumerate(self.grid):
            for x, cellVar in enumerate(row):
                if valRange:
                    if cellVar.getMode() >= content:
                        foundCells.append(cellVar)
                else:
                    if cellVar.getMode() == content:
                        foundCells.append(cellVar)
        return foundCells

    def fetchCell(self, xAxis: int, yAxis: int) -> cell:
        """Returns the cell at the given coordinates, or a default invalid cell if out of bounds"""
        if yAxis < 0:
            return cell(-1, -1, -1)
        if yAxis >= len(self.grid):
            return cell(-1, -1, -1)
        row = self.grid[yAxis]
        if xAxis < 0:
            return cell(-1, -1, -1)
        if xAxis >= len(row):
            return cell(-1, -1, -1)
        return row[xAxis]

    def fetchNeighbours(self, xAxis: int, yAxis: int):
        """
        Returns a dict of jumping direction containing:
        the start cell, the cell being jump, with the x/y being the end point
        """
        # endPoint = self.fetchCell(xAxis, yAxis)
        northJump = self.fetchCell(xAxis, yAxis - 1)
        northStart = self.fetchCell(xAxis, yAxis - 2)

        southJump = self.fetchCell(xAxis, yAxis + 1)
        southStart = self.fetchCell(xAxis, yAxis + 2)

        eastJump = self.fetchCell(xAxis + 1, yAxis)
        eastStart = self.fetchCell(xAxis + 2, yAxis)

        westJump = self.fetchCell(xAxis - 1, yAxis)
        westStart = self.fetchCell(xAxis - 2, yAxis)

        # 'start' will jump over 'jump' and end at 'end'
        # 1 - 2 - 0
        # 0 - 0 - 1
        neighbours = {
            "south": (northStart, northJump),
            "north": (southStart, southJump),
            "west": (eastStart, eastJump),
            "east": (westStart, westJump),
        }
        return neighbours

    def validMoves(self) -> list[tuple[cell, str]]:
        moves = []
        emptyCells = self.fetchCellContent(0)
        for endPoint in emptyCells:
            x, y = endPoint.getPos()
            neighbours = self.fetchNeighbours(x, y)
            for direction in neighbours.keys():
                directionNeighbour = neighbours[direction]
                beingJumped = directionNeighbour[1]
                startPoint = directionNeighbour[0]
                if beingJumped.getMode() >= 1 and startPoint.getMode() >= 1:
                    moves.append((startPoint, direction))
        return moves

    def displayMoves(self):
        moves = self.validMoves()
        id = 1
        for i in moves:
            x, y = i[0].getPos()
            mode = i[0].getMode()
            dir = i[1]
            print(f"{id}:\tX: {x+1}\t Y: {y+1}\t Dir: {dir}\t Mode: {mode}")
            id += 1
        return moves

    def makeMove(self, x: int, y: int, directon: str):
        newDir = self.invertDirMap[directon]
        startPoint = self.fetchCell(x, y)
        neighbours = self.fetchNeighbours(x, y)

        valid = neighbours[newDir]
        beingJumped = valid[1]
        endPoint = valid[0]

        if not startPoint.validCell():
            return False
        if not beingJumped.validCell():
            return False
        if not endPoint.validCell():
            return False

        self.changeCellModeByCell(startPoint, 0)
        self.changeCellModeByCell(beingJumped, 0)
        self.changeCellModeByCell(endPoint, 1)

        return True

    def hasWon(self) -> bool:
        occupiedCell = self.fetchCellContent(1, True)
        if len(occupiedCell) != 1:
            return False
        elif occupiedCell[0].getMode() != 1:
            return False
        elif len(occupiedCell) == 1 and occupiedCell[0].getMode() == 1:
            return True
        else:
            return False

    def encodeGrid(self) -> str:
        BASE = self.BASE
        segmentSize = self.segmentSize
        flattenGrid = [x for xs in self.grid for x in xs]
        totalSegments = math.ceil(len(flattenGrid) / segmentSize)

        modeMap = {-1: 1, 0: 2, 1: 3}
        encodedValue = [
            str(self.width),
            "-",
            str(self.height),
            "-",
            str(segmentSize),
            "-",
        ]
        for segmentNum in range(totalSegments):
            low = segmentSize * segmentNum
            high = (segmentSize * segmentNum) + segmentSize
            segment = flattenGrid[low:high]

            encodedNum = 0
            for segmentIndex, x in enumerate(segment):
                mappedMode = modeMap.get(x.getMode(), 3)
                factor = BASE**segmentIndex
                encodedNum += (factor * mappedMode) - factor

            encodedSegment = self.encodeList[encodedNum]
            encodedValue.append(encodedSegment)
        return "".join(encodedValue)

    def _encodeGridStatic(self, grid: list[list[cell]]) -> str:
        """Encodes a given grid without modifying self"""
        BASE = self.BASE
        segmentSize = self.segmentSize
        flattenGrid = [x for xs in grid for x in xs]
        totalSegments = math.ceil(len(flattenGrid) / segmentSize)

        modeMap = {-1: 1, 0: 2, 1: 3}
        encodedValue = [
            str(self.width),
            "-",
            str(self.height),
            "-",
            str(segmentSize),
            "-",
        ]
        for segmentNum in range(totalSegments):
            low = segmentSize * segmentNum
            high = (segmentSize * segmentNum) + segmentSize
            segment = flattenGrid[low:high]

            encodedNum = 0
            for segmentIndex, x in enumerate(segment):
                mappedMode = modeMap.get(x.getMode(), 3)
                factor = BASE**segmentIndex
                encodedNum += (factor * mappedMode) - factor

            encodedSegment = self.encodeList[encodedNum]
            encodedValue.append(encodedSegment)
        return "".join(encodedValue)

    def decodeGrid(self, encodedGrid, segmentSize):
        BASE = self.BASE
        fullGrid = []
        modeMap = {1: -1, 2: 0, 3: 1}

        for code in encodedGrid:
            segment = []
            reverseMap = self.encodeDict.get(code, 0)  # O(1) lookup instead of O(n)
            remainder = reverseMap
            for i in range(segmentSize - 1, -1, -1):
                factor = BASE**i
                mode = int((remainder / factor) + 1)
                remainder = remainder % factor
                mappedMode = modeMap.get(mode, -1)
                segment.insert(0, mappedMode)
            fullGrid += segment

        return fullGrid

    def decodeAndApply(self, code):
        width, height, segmentSize, encodedGrid = code.split("-")
        width = int(width)
        height = int(height)
        segmentSize = int(segmentSize)

        self.width = width
        self.height = height
        decodedGrid = self.decodeGrid(encodedGrid, segmentSize)
        newGrid = []
        for y in range(self.height):
            newRow = []
            low = self.width * y
            high = (self.width * y) + self.width
            row = decodedGrid[low:high]
            for x, mode in enumerate(row):
                newRow.append(cell(x, y, mode))
            newGrid.append(newRow)

        self.grid = newGrid
        # return newGrid

    def rotateGrid90(self):
        """Rotate grid 90 degrees clockwise"""
        newGrid = list(zip(*self.grid[::-1]))
        # newGrid = np.rot90(self.grid)
        self.grid = newGrid

    def _rotateGrid90Static(self, grid: list[list[cell]]) -> list[list[cell]]:
        """
        Rotate grid 90 degrees clockwise
        returns a new grid without modifying self.grid
        """
        return [list(row) for row in zip(*grid[::-1])]

    def reflectGrid(self, mode=0):
        """
        Reflect grid
        mode = 0, flips along horizontal, top to bottom
        mode = 1, flips along vertical, left to right
        """
        newGrid = [row[::-1] for row in self.grid]
        # newGrid = np.flip(self.grid, mode)
        # for y in range(self.height):
        #     newRow = self.grid[y]
        #     flippedRow = newRow[::-1]
        #     newGrid.append(flippedRow)
        self.grid = newGrid

    def _reflectGridStatic(self, grid) -> list[list[cell]]:
        """
        Reflect grid vertically
        returns a new grid without modifying self.grid
        """
        return [row[::-1] for row in grid]

    def getConicalForm(self):
        """
        Get canonical form by checking all 8 symmetries without modifying self.grid
        """
        forms = set()
        grid = self.grid

        for _ in range(2):
            for _ in range(4):
                grid = self._rotateGrid90Static(grid)
                forms.add(self._encodeGridStatic(grid))
            grid = self._reflectGridStatic(grid)

        return min(forms)


def openJson(fileName: str) -> dict:
    import json

    try:
        with open(fileName, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    except Exception as e:
        print(f"Error loading JSON: {e}")
        data = {}
    return data


def saveJson(fileName: str, data: dict) -> None:
    import json

    try:
        with open(fileName, "w") as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        print(f"Error saving JSON: {e}")


def deepSearch(startGame: table, depth=5, initialMap=None, visited=None) -> dict:
    """
    Performs a depth-first search of the game state space starting from startGame, exploring all valid moves up to a specified depth.
    It builds a mapping of game states to their reachable next states, while avoiding cycles by tracking visited states.
    The function returns a dictionary where each key is a game state and its value is a list of states that can be reached from it in one move,
    along with special markers for winning or losing end states.
    """

    if initialMap is None:
        initialMap = {}
    if visited is None:
        visited = set()

    startStateEncoded = startGame.getConicalForm()

    if startStateEncoded in initialMap:
        nextStates = initialMap.get(startStateEncoded)
        if nextStates:
            return initialMap

    # Skip if already visited to prevent cycles and redundant exploration
    if startStateEncoded in visited:
        return initialMap

    visited.add(startStateEncoded)
    moves = startGame.validMoves()
    initialMap.update({startStateEncoded: []})

    for go in moves:
        endState = deepcopy(startGame)
        x, y = go[0].getPos()
        result = endState.makeMove(x, y, go[1])

        if result:
            endStateEncoded = endState.getConicalForm()

            if endStateEncoded not in initialMap[startStateEncoded]:
                initialMap[startStateEncoded].append(endStateEncoded)

            if depth > 0:
                # print(depth)
                initialMap = deepSearch(endState, depth - 1, initialMap, visited)

    if not moves:
        if startGame.hasWon():
            initialMap[startStateEncoded].append("WIN")
            print(startStateEncoded)
        else:
            initialMap[startStateEncoded].append("END")
            # print("end")
    return initialMap


def initializeSearch(gameMap, repeats, depth=5):
    """Initializes the search by starting from random states in the game map, including unlinked states, to discover more of the state space and potentially find new paths to win or end states."""
    for _ in range(repeats):
        blankTable = table()
        startMap = blankTable.getConicalForm()
        if startMap in gameMap:
            unlinkedMaps = find_unlinked_states(gameMap)
            newStartMap = random.choice(unlinkedMaps) if unlinkedMaps else startMap
            blankTable.decodeAndApply(newStartMap)
        #     print(f"Starting from an unlinked state: {newStartMap}")
        # else:
        #     print(f"Starting from state: {startMap}")

        s1Time = time()
        results = deepSearch(blankTable, depth, initialMap=gameMap)
        e1Time = time()
        # print(f"Search took {e1Time - s1Time} seconds")
        gameMap.update(results)

    return gameMap


def build_reverse_map(graph: dict[str, list[str]]) -> dict[str, list[str]]:
    """Flips all edges in the graph so we can traverse backwards."""
    reverse = defaultdict(list)
    for parent, children in graph.items():
        for child in children:
            reverse[child].append(parent)
    return reverse


def findPaths(graph: dict[str, list[str]], start: str, end: str) -> list[list[str]]:
    """
    Finds all paths from start to end
    and walking backwards from end to start.
    Returns each path in start -> end order.
    """
    reverseGraph = build_reverse_map(graph)
    all_paths = []

    def backtrack(current: str, path: list[str]):
        if current == start:
            all_paths.append(list(reversed(path)))
            return
        allParents = reverseGraph.get(current, [])
        for parent in allParents:
            if parent not in path:  # avoid cycles
                path.append(parent)
                backtrack(parent, path)
                path.pop()

    backtrack(end, [end])
    return all_paths


def find_unlinked_states(search_results: dict[str, list[str]]) -> list[str]:
    """Return state strings that are not linked to anything."""

    unlinked: list[str] = []
    # visited = set()

    for parent, endStates in search_results.items():
        # if parent in visited:
        #     continue

        if not endStates:
            unlinked.append(parent)
            # visited.add(parent)
            continue

        if "WIN" in endStates or "END" in endStates:
            # visited.add(parent)
            continue

        for state in endStates:
            # visited.add(state)
            if state not in search_results:
                unlinked.append(state)

    return unlinked


def displayPaths(paths: list[list[str]], pathType: str):
    if len(paths) <= 10:
        if paths:
            print(f"Paths from start to {pathType}:")
            for path in paths:
                print(" -> ".join(path))
        else:
            print(f"No paths found from start to {pathType}.\n")
    else:
        print(f"{len(paths)} paths found from start to {pathType}, not printing all.\n")


def startSearch(gameTable: table):
    """Play ground function for testing and other stuff"""
    # setup
    fileName = f"S{gameTable.segmentSize}_results.json"
    gameMap = openJson(fileName)
    startMap = gameTable.getConicalForm()
    print(f"Starting search\n")

    #

    # search from a specified starting state, then searches until depth is reached.
    # s1Time = time()
    # results = deepSearch(gameTable, depth, initialMap=gameMap)
    # e1Time = time()
    # print(f"Search took {e1Time - s1Time} seconds\n")

    # explore the game space

    # Explore the state space by starting from random states in the game map, including unlinked states, to discover more of the state space and potentially find new paths to win or end states.
    s1Time = time()
    repeats = 50
    depth = 8
    results = initializeSearch(gameMap, repeats, depth=depth)
    e1Time = time()
    print(f"Initialization and search took {e1Time - s1Time} seconds\n")

    # save results to file

    s2Time = time()
    gameMap.update(results)
    saveJson(fileName, gameMap)
    e2Time = time()
    print(f"Saving took {e2Time - s2Time} seconds\n")

    # searches for paths to end states

    s3Time = time()
    # paths = findPaths(results, start=startMap, end="END")
    paths = []
    e3Time = time()
    print(f"Finding 'end' paths took {e3Time - s3Time} seconds")
    displayPaths(paths, "end")

    # searches for winnable paths

    s4Time = time()
    paths = findPaths(results, start=startMap, end="WIN")
    e4Time = time()
    print(f"Finding 'win' paths took {e4Time - s4Time} seconds")
    displayPaths(paths, "win")

    # display some stats about the search results

    print(f"Total unique starting states found: {len(results)}")


def play(gameTable: table):
    gameTable.applyTable("play")
    DEPTH = 5
    while True:
        gameTable.displayTable()
        moves = gameTable.displayMoves()
        # moves = gameTable.validMoves()

        options = {}
        id = 1
        for cellVar, dir in moves:
            x, y = cellVar.getPos()
            option = (x, y, dir)
            options.update({id: option})
            id += 1

        choice = -1
        while choice not in options.keys():
            choice = int(
                input(
                    f"From the list above choose an option, top is 1 or -1 to check if you can win within {DEPTH} moves: "
                )
            )

            if choice == -1:
                # break
                allMoves = deepSearch(gameTable, DEPTH)
                paths = findPaths(allMoves, start=gameTable.getConicalForm(), end="WIN")
                if paths:
                    print(f"Can win in {DEPTH} moves or less!")
                else:
                    print(f"Cannot win in {DEPTH} moves or less.")
                for path in paths:
                    print("Paths from start to Win:")
                    print(" -> ".join(path))

        option = options.get(choice)
        if not option:
            print("Error")
            break
        print(f"Doing move: {option}")
        gameTable.makeMove(option[0], option[1], option[2])


def testPath(path: list[str]):
    gameTable = table()
    for state in path:
        gameTable.decodeAndApply(state)
        gameTable.displayTable()


if __name__ == "__main__":

    blankTable = table()

    startSearch(blankTable)

    # a = []
    # testPath(a)

    # play(blankTable)
