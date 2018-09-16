# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def start_link():
    """Create the url of the starting page to be crawled.

    Returns:
    page_to_crawl: string of the starting website
    """
    # Create tomorrows day date if time past xxx, and add it to the
    # standard url (tomorrow matches) otherwise take standard url
    # (today's matches)
    # In the evening the users would like to know the matches of the next day
    evening_crawl_time = datetime.strptime("your time", "%H:%M").time()

    if datetime.now().time() > evening_crawl_time:
        tomorrow = datetime.today().date() + timedelta(days=1)
        page_to_crawl = "url" + str(tomorrow)
    else:
        page_to_crawl = "url"

    return page_to_crawl


"""The version number"""
__version__ = "0.1"
