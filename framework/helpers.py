import urllib.parse


def parsed(hero_name):
    return urllib.parse.quote_plus(hero_name)
