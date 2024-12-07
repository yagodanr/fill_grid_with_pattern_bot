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
    debug(f"parse_field -> {field}")
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
    for _ in range(height):
        l = input()
        debug(f"Piece: {l}")
        figure.append([])
        for el in l:
            if el == "*":
                figure[-1].append(1)
            else:
                figure[-1].append(0)
    debug(f"parse_figure -> returns: {(height, width), figure}")
    return (height, width), figure


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    move = None
    size = parse_field_info()
    field = parse_field(size)
    figure_size, figure = parse_figure()
    return move


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
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
