# -*- coding: utf-8 -*-

import re
from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import crawler_functions as cf


def link_crawl(str_players, page_to_crawl):
    """Crawl website for match information and check if player link is relevant.

    Arguments:
    str_players: string with all relevant players names
    page_to_crawl: string of the start website to crawl

    Returns:
    links_n_matches: list of matches with possible relevant player links and
    match information (tournament name, time match starts and odds)
    """
    # The code runs twice as the crawler sometimes randomly misses matches
    links_n_matches = []
    for i in range(2):
        # For second round create list of all matches which have already been
        # collected matches aren't appended twice
        if i != 0:
            links_check = [x[:] for x in links_n_matches]
        else:
            links_check = []

        # Initiate crawling
        driver = webdriver.PhantomJS(executable_path="/your_folders/bin/phantomjs")
        driver.get(page_to_crawl)
        driver.maximize_window()

        # Crawler starts on tournament level and extracts tournament info
        for tournament in cf.elements_xpath(driver, driver, "//div[@class='event-list-table-wrapper js-event-list-table-wrapper']/descendant::div[@class='js-event-list-tournament tournament']"):
            tournament_name = cf.element_class(driver, tournament, "tournament__name")
            # Crawler goes a level deeper onto match level within tournament
            matches = cf.elements_class(driver, tournament, "list-event")
            # Since we experience sometimes a StaleElementReferenceException,
            # we have to loop and try/except with a count so that the crawler
            # can continue at the same match where we experienced a
            # StaleElementReferenceException
            counter = 0
            while counter < len(matches):
                try:
                    match = matches[counter]
                    # Extract the time of the match and change it bcz AWS
                    # server is two hours behind where I live :-)
                    status = cf.element_class(driver, match, "status")
                    status_split = status.strip().replace("\n", " ").split(":")
                    if status_split[0].isdigit():
                        hours = datetime.strptime(status_split[0], "%H") + timedelta(hours=2)
                        match_time = hours.strftime("%H") + ":" + status_split[1]
                    else:
                        # Sometime match time is word like "2. set"
                        match_time = status
                    # Click on match element to get onto player level
                    match.click()
                    sleep(0.5)
                    # Extract player links per match and append to link list
                    links = cf.elements_xpath(driver, driver, "//div[@class='js-event-widget-header-container']/descendant::div/descendant::div/descendant::div/descendant::a")
                    player_links = [link.get_attribute("href") for link in links if "team" in link.get_attribute("href")]
                    # Extract odds per match (if there are any) and append to
                    # odds list
                    odds = cf.elements_xpath(driver, driver, "//div[@class='js-event-page-odds-container']/descendant::span[@class='js-odds-value-decimal']")
                    if odds is not None:
                        #odds get update, so we want the newest ones in [:2]
                        players_odds = [odd.get_attribute("textContent").strip() for odd in odds[:2]]
                    else:
                        players_odds = []
                    # Check if name in the player link (extract with regex) is
                    # in str_players and therefore possibly relevant (can have
                    # duplicates so we have to make latter on a second check
                    # with the individual full names but the list of player
                    # links for the full name get shortend down drastically
                    # this way)
                    # Also check if match hasn't already been appended
                    # Also check if latest match hasn't been appended just
                    # before (sometimes crawler creates duplicates)
                    for player_link in player_links:
                        if (re.search(r"(\w+)-", player_link).group(1).capitalize() in str_players
                                and links_n_matches == []):
                                    links_n_matches.append([player_links, tournament_name, match_time, players_odds])
                        elif (re.search(r"(\w+)-", player_link).group(1).capitalize() in str_players
                              and [player_links, tournament_name, match_time, players_odds] not in links_check
                                and player_links not in links_n_matches[-1]):
                                    links_n_matches.append([player_links, tournament_name, match_time, players_odds])
                    counter += 1
                except StaleElementReferenceException:
                    matches = cf.elements_class(driver, tournament, "list-event")
        driver.quit()
    return links_n_matches


'''The version number'''
__version__ = "0.1"
