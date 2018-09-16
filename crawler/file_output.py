# -*- coding: utf-8 -*-

import pandas as pd


def file_output(games, list_players):
    """
    Check if players of a game are relevant and create csv based on df.

    Arguments:
    games: list with all the relevant matches containing player names,
    tournament name, game time and odds
    list_players: list with all players that are relevant

    Creates:
    csv: based on df with each line representing a relevant match,
    containing player names, tournament name, game time and odds
    """
    # Create df and fill rows with the relevant matches and create csv output
    # Columns are in German for the users (Gegner = Opponent, Turnier =
    # tournament, Zeit = time, Kommentar = Comment)
    df = pd.DataFrame(columns=["Player", "Doubles Partner", "Gegner",
                               "Turnier", "Zeit", "Quote 1", "Quote 2",
                               "Kommentar"])
    # Go through games list
    for info in games:
        # Check if a game is single or doubles game (len(6) ==singles game)
        # and if one of the players is in relevant players list.
        # If yes, append game to df.
        if (len(info) == 6 and info[0] in list_players):
            df = df.append({"Player": info[0], "Doubles Partner": "",
                            "Gegner": info[1], "Turnier": info[2],
                            "Zeit": info[3], "Quote 1": info[4],
                            "Quote 2": info[5],
                            "Kommentar": ""}, ignore_index=True)
        elif (len(info) == 6 and info[1] in list_players):
            df = df.append({"Player": info[1], "Doubles Partner": "",
                            "Gegner": info[0], "Turnier": info[2],
                            "Zeit": info[3], "Quote 1": info[5],
                            "Quote 2": info[4],
                            "Kommentar": ""}, ignore_index=True)
        elif len(info) != 6:
            if info[0] in list_players:
                df = df.append({"Player": info[0], "Doubles Partner": info[1],
                                "Gegner": "%s, %s" % (info[2], info[3]),
                                "Turnier": info[4], "Zeit": info[5],
                                "Quote 1": info[6], "Quote 2": info[7],
                                "Kommentar": ""}, ignore_index=True)
            if info[1] in list_players:
                df = df.append({"Player": info[1], "Doubles Partner": info[0],
                                "Gegner": "%s, %s" % (info[2], info[3]),
                                "Turnier": info[4], "Zeit": info[5],
                                "Quote 1": info[6], "Quote 2": info[7],
                                "Kommentar": ""}, ignore_index=True)
            if info[2] in list_players:
                df = df.append({"Player": info[2], "Doubles Partner": info[3],
                                "Gegner": "%s, %s" % (info[0], info[1]),
                                "Turnier": info[4], "Zeit": info[5],
                                "Quote 1": info[7], "Quote 2": info[6],
                                "Kommentar": ""}, ignore_index=True)
            if info[3] in list_players:
                df = df.append({"Player": info[3], "Doubles Partner": info[2],
                                "Gegner": "%s, %s" % (info[0], info[1]),
                                "Turnier": info[4], "Zeit": info[5],
                                "Quote 1": info[7], "Quote 2": info[6],
                                "Kommentar": ""}, ignore_index=True)
    # Sort df by time and turn df to a csv
    df = df.sort_values(by='Zeit', ascending=True)
    df.to_csv("/your_folders/your_file_name.csv",
              sep=",", encoding="utf-8")


"""The version number"""
__version__ = "0.1"
