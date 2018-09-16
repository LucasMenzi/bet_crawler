# -*- coding: utf-8 -*-

import csv
import unidecode


def lookup(path):
    """Create look up list and look up list string of relevant players.

    Arguments:
    path: path to the csv file with the relevant players to extract

    Returns:
    list_players: list with the relevant players full names as string
    str_players: names of the relevant players as one string (reason behind
    that: we can shorten the list of player links to be crawled. Bcz the last
    name is in the player link and we can look up that word in the str_players
    string)
    """
    # Read csv file and return lookup list and lookup string
    with open(path, newline="", encoding="utf-8") as f:
        list_players = []
        reader = csv.reader(f)
        for row in reader:
            list_players.append(row[0].strip())
        str_players = unidecode.unidecode(" ".join(list_players))
    return (list_players, str_players)


"""The version number"""
__version__ = "0.1"
