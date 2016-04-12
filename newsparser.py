from newssiteparser import ArticleCollector, NewsSiteParser, ArticleScraper
import pprint
import sys
import argparse
import re
import datetime


def parse_month_year(date_string):
    """
    Parses a date string of the form mm/yyyy and returns a tuple of the form
    (month, year)
    :param date_string:
    :return:
    """
    date_regex = re.compile(r"(\d{2})\/(\d{4})")

    matches = date_regex.findall(date_string)

    if matches is None:
        print "Start and end dates must be of the form mm/yyyy"
        exit()

    return matches[0]


parser = argparse.ArgumentParser()

parser.add_argument('-s', action='store', dest='start_date_string',
                    help='Start date for parsing eg. mm/yyyy. Default is 01/2002.')

parser.add_argument('-e', action='store', dest='end_date_string',
                    help='End date for parsing eg. mm/yyyy. Default is current month.')

parser.add_argument('-i', action='store', dest='start_index', type='int',
                    help='The starting index for post and image IDs. Default is 0')

results = parser.parse_args()

start_index = results.start_index or 0

now = datetime.datetime.now()

if results.start_date_string is not None:
    start_month_year = parse_month_year(results.start_date_string)
else:
    start_month_year = ('01', '2002')

if results.end_date_string is not None:
    end_month_year = parse_month_year(results.end_date_string)
else:
    end_month_year = ("%02d" % (now.month,), str(now.year))

if int(start_month_year[1]) > int(end_month_year[1]):
    print "newsparser: Start date may not be after end date"
    exit()
if int(start_month_year[1]) == int(end_month_year[1]) and int(start_month_year[0]) > int(end_month_year[0]):
    print "newsparser: Start date may not be after end date"
    exit()

nsp = NewsSiteParser(start_index=start_index)

nsp.run(start_month_year[0], start_month_year[1], end_month_year[0], end_month_year[1])
