import math
from copy import deepcopy


class cell:
    def __init__(self, x: int, y: int, mode: int = -1) -> None:
        self.x = x
        self.y = y
        self.mode = mode

    def getMode(self) -> int:
        return self.mode

    def getPos(self) -> tuple[int, int]:
        return (self.x, self.y)

    def changeMode(self, newMode: int) -> None:
        self.mode = newMode

    def validCell(self) -> bool:
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
        ]

    def fetchTable(self):
        return self.grid

    def changeCellMode(self, xAxis, yAxis, mode):
        cell = self.grid[yAxis][xAxis]
        cell.changeMode(mode)

    def createTable(self):
        grid = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                row.append(cell(x, y))
            grid.append(row)
        return grid

    def applyTable(self, mode="play"):
        if mode == "play":
            for y, row in enumerate(self.grid):
                for x, cellVar in enumerate(row):
                    if y in [0, 1, 5, 6]:
                        if x in [2, 3, 4]:
                            cellVar.changeMode(1)
                    elif y in [2, 3, 4]:
                        cellVar.changeMode(1)
            self.changeCellMode(3, 3, 0)

        elif mode == "debug":
            increment = 1
            for y, row in enumerate(self.grid):
                for x, cellVar in enumerate(row):
                    if y in [0, 1, 5, 6]:
                        if x in [2, 3, 4]:
                            cellVar.changeMode(increment)
                            increment += 1
                    elif y in [2, 3, 4]:
                        cellVar.changeMode(increment)
                        increment += 1
            self.changeCellMode(3, 3, 0)

    def displayTable(self):
        for row in self.grid:
            stringVar = ""
            for cellVar in row:
                stringVar += f"\t{cellVar.getMode()}"
            print(stringVar)

    def fetchCellContent(self, content=0) -> list[cell]:
        foundCells = []
        for y, row in enumerate(self.grid):
            for x, cellVar in enumerate(row):
                if cellVar.getMode() == content:
                    foundCells.append(cellVar)
        return foundCells

    def fetchCell(self, xAxis: int, yAxis: int) -> cell:
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
        Docstring for fetchNeighbours

        :param xAxis: Description
        :type xAxis: int
        :param yAxis: Description
        :type yAxis: int
        Return
        a dict of jumping direction containing:
        the start cell, the cell being jump, with the x/y being the end point
        """
        endPoint = self.fetchCell(xAxis, yAxis)
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

        startPoint.changeMode(0)
        beingJumped.changeMode(0)
        endPoint.changeMode(1)

        return True

    def encodeGrid(self):
        BASE = 3
        bitDepth = len(self.encodeList)  # potential bit depth
        segmentSize = int(
            math.log(bitDepth) // math.log(BASE)
        )  # highest available segment size, if bitdepth is 50, it can support 4 segment size cause 3**4 == 81
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

            # print(encodedNum)
            encodedSegment = self.encodeList[encodedNum]
            encodedValue.append(encodedSegment)
        return "".join(encodedValue)

    def decodeGrid(self, encodedGrid, segmentSize):
        BASE = 3
        fullGrid = []
        modeMap = {1: -1, 2: 0, 3: 1}

        for code in encodedGrid:
            segment = []
            reverseMap = self.encodeList.index(code)
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
        return newGrid

    def hasWon(self) -> bool:
        occupiedCell = self.fetchCellContent(1)
        if len(occupiedCell) != 1:
            return False
        elif occupiedCell[0].getMode() != 1:
            return False

        else:
            return True


def play(gameTable: table):
    gameTable.applyTable("play")
    while True:
        gameTable.displayTable()
        gameTable.displayMoves()
        moves = gameTable.validMoves()

        options = {}
        id = 1
        for cellVar, dir in moves:
            x, y = cellVar.getPos()
            option = (x, y, dir)
            options.update({id: option})
            id += 1

        choice = -1
        while choice < 1:
            choice = int(input("From the list above choose an option, top is 1: "))

        option = options.get(choice)
        if not option:
            print("Error")
            break
        print(f"Doing move: {option}")
        gameTable.makeMove(option[0], option[1], option[2])


if __name__ == "__main__":

    gameMap = {}

    a = table()

    # a.displayTable()
    #
    # b = a.encodeGrid()
    # print(b)
    # a.decodeAndApply(b)
    #
    # a.displayTable()

    # a.displayTable()
    # a.displayMoves()

    # result = a.makeMove(3, 5, "north")
    # print(result)

    # a.displayTable()
    # a.displayMoves()

    play(a)
