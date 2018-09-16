# -*- coding: utf-8 -*-

from selenium import webdriver
import crawler_functions as cf


def full_names_crawl(links_n_matches, list_players):
    """Crawl player pages for their full name and append if name is relevant.

    Arguments:
    links_n_matches: list with the crawled matches containing player links,
    tournament name, game time and odds
    list_players: list with all players that are relevant

    Returns:
    games: list with the relevant matches containing player names, tournament
    name, game time and odds
    """
    # Initiate webdriver and games list
    driver = webdriver.PhantomJS(executable_path="/your_folders/bin/phantomjs")
    games = []
    # Go through all the matches in links_n_matches
    for match in links_n_matches:
        names = []
        # Go through every player link in a match to extract the players full
        # name from his website and append to names
        for link in match[0]:
            driver.get(link)
            driver.maximize_window()
            name = cf.element_class(driver, driver, "page-title").strip().encode("utf-8")
            names.append(name.decode("utf-8"))
        # Check every name if its in relevant list_players and if odds are
        # present. Append match to games if one name in the match is relevant
        odds = [m3.encode("utf-8") for m3 in match[3]]
        for n in names:
            if (n in list_players and odds != []):
                tournament = match[1].encode("utf-8")
                time = match[2].encode("utf-8")
                games.append(names
                             + [tournament.decode("utf-8")]
                             + [time.decode("utf-8")]
                             + [odd.decode("utf-8") for odd in odds])
                break
            if (n in list_players and odds == []):
                tournament = match[1].encode("utf-8")
                time = match[2].encode("utf-8")
                games.append(names
                             + [tournament.decode("utf-8")]
                             + [time.decode("utf-8")]
                             + ["", ""])
                break
            else:
                continue
    driver.quit()
    return games


"""The version number"""
__version__ = "0.1"
