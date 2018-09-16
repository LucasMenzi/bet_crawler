# -*- coding: utf-8 -*-

"""Deploy all functions and send relevant matches or exception by mail."""

from datetime import datetime, timedelta
import mail as m
import start_link as sl
import lookup as lu
import file_output as fo
import link_crawl as lc
import full_names_crawl as fnc


# Mail telling that the program is has started to run
m.mail(["your email"], ["started"], "program has started")

# Generall try/except block, bcz sometimes changes to website to be crawled
# can cause different exceptions
try:
    # Create list and string with the relevant players for matches to bet on
    path = "/your_folders/data/lookup_players.csv"
    list_players = lu.lookup(path)[0]
    str_players = lu.lookup(path)[1]

    # Create start page that needs to be crawled
    page_to_crawl = sl.start_link()

    # Extract the players links and check if part of the names are in
    # str_players
    links_n_matches = lc.link_crawl(str_players, page_to_crawl)
    print(len(links_n_matches))

    # Extract full names of the players in links_n_matches and get all the
    # games with relevant players in list_players
    games = fnc.full_names_crawl(links_n_matches, list_players)
    print(len(games))

    # Create csv output with the relevant matches as attachments for mail
    fo.file_output(games, list_players)
    output = "/your_folders/your_file_name.csv"

    # Send e-mail to...
    emailto = ["your email"]

    # E-Mail Subject definition
    evening_crawl_time = datetime.strptime("your time", "%H:%M").time()
    if datetime.now().time() < evening_crawl_time:
        today = str(datetime.today().date())
        betreff = "Matches on the {}".format(today)
    else:
        next_day = str(datetime.today().date() + timedelta(days=1))
        betreff = "Matches on the {}".format(next_day)
    m.mail(emailto, output, betreff)

except Exception as argument:
    arg = [str(argument)]
    m.mail(["your email"], arg, "Exception")


"""The version number"""
__version__ = "0.1"
