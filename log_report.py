#!/usr/bin/env python3

import psycopg2

DBNAME = "news"


def report_most_popular_articles_ever():
    """ Reports the most popular articles """
    db = psycopg2.connect(database=DBNAME)
    print("What are the most popular three articles of all time?")
    c = db.cursor()
    c.execute("SELECT * FROM most_popular_articles_ever ORDER BY count DESC;")
    results = c.fetchall()
    db.close()

    for result in results:
        print("'%s' — %s views" % (result[1], result[0]))

    print("\n")


def report_most_popular_authors_ever():
    """ Reports the most popular authors """
    db = psycopg2.connect(database=DBNAME)
    print("Who are the most popular article authors of all time?")
    c = db.cursor()
    c.execute("SELECT * FROM most_popular_authors ORDER BY count DESC;")
    results = c.fetchall()
    db.close()

    for result in results:
        print("%s — %s views" % (result[0], result[1]))

    print("\n")


def report_request_errors():
    """ Reports the days with more than 1% error rate """
    db = psycopg2.connect(database=DBNAME)
    print("On which days did more than 1% of requests lead to errors?")
    c = db.cursor()
    c.execute("SELECT * FROM requests_error ORDER BY day;")
    results = c.fetchall()
    db.close()

    for result in results:
        print("%s — %s%% errors" % (result[0], result[1]))

    print("\n")


if __name__ == '__main__':
    print("##### Log-Analysis-Tool #####")
    report_most_popular_articles_ever()
    report_most_popular_authors_ever()
    report_request_errors()
