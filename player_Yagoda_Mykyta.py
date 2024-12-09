#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info() -> tuple[int, int]:
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    debug(f"Description of the field: {l}")
    tmp = l.strip().strip(":").split()
    height = int(tmp[1])
    width = int(tmp[2])
    return height, width

def parse_field(size: tuple[int, int]) -> list[str]:
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowercase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    """
    field = [[0]*size[1] for _ in range(size[0])]

    #cuts the first row of column numbers
    l = input()
    debug(f"Field: {l}")
    for i in range(size[0]):
        l = input()
        debug(f"Field: {l}")
        field[i] = l.split()[1]
    # debug(f"parse_field -> {field}")
    return field


def parse_figure() -> tuple[tuple[int, int], list[list[int]]]:
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    l = input()
    debug(f"Piece: {l}")
    l = l.strip().strip(":").split()
    *_, height, width = l
    height = int(height)
    width = int(width)
    figure = []
    right_end = 0
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")
        figure.append(l)
        right_end = max(right_end, l.rfind("*"))
    width = right_end + 1
    for bottom in range(height-1, 0-1, -1):
        if figure[bottom].strip(".") != "":
            break
    figure = figure[:bottom+1]
    figure = [line[:right_end+1] for line in figure]

    # debug(f"parse_figure -> returns: {(len(figure), width), figure}")
    return (len(figure), width), figure

def make_move(field_size: tuple[int, int], field: list[str],
              figure_size: tuple[int, int], figure: list[str],
              player: int) -> tuple[int, int]:
    """
    takes a lot of parameters and about game state and returns move for given player

    Returns:
        tuple[int, int]: move
    """

    player_symbol = "o" if player == 1 else "x"
    opponent_symbol = "x" if player == 1 else "o"

    def generate_moves() -> list[tuple[int, int]]:
        moves = []
        for i in range(field_size[0]-figure_size[0]+1):
            for j in range(field_size[1]-figure_size[1]+1):
                overlap = 0
                # debug(f"=====i, j -> {i, j}=======")
                # if i > 5 or j > 5:
                #     break

                for f_i in range(figure_size[0]):
                    for f_j in range(figure_size[1]):
                        x, y = i + f_i, j + f_j
                        el = None
                        try:
                            el = field[x][y]
                        except IndexError:
                            break
                        el = el.lower()
                        # debug(f"x, y -> {x, y}")

                        if figure[f_i][f_j] == ".":
                            continue

                        if el == player_symbol:
                            overlap += 1
                        elif el != '.':
                            break

                        if overlap > 1:
                            break

                    else:
                        continue
                    break
                else:
                    if overlap == 1:
                        moves.append((i, j))
        debug(f"moves -> {moves}")
        return moves


    moves = generate_moves()
    if len(moves) == 0:
        return None
    debug(f"make_move -> {moves}")


    def principle(coord):
        x, y = coord
        right, bottom = x + figure_size[0], y + figure_size[1]


        return min([min(abs(x-i), abs(right-i))+min(abs(y-j), abs(bottom-j))
                for i in range(field_size[0])
                for j in range(field_size[1]) if field[i][j].lower() == opponent_symbol])
    return min(moves, key=principle)


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    size = parse_field_info()
    field = parse_field(size)
    figure_size, figure = parse_figure()


    move = make_move(size, field, figure_size, figure, player)



    return move


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        if move is None:
            print(None)
            break
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    debug(f"Info about the player: {i}")
    return 1 if "p1 :" in i else 2


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()