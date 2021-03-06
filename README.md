# ud-log-analysis
The program is written in python3. To connect to the database, psycopg2 is used. To run the program, use: `python3 log_report.py`. The views whose create statements are shown below need to be created in advance.

An example output is shown in `example_output.txt`.

## Views
The following views need to be created in order to run the program.

### What are the most popular three articles of all time? 
    CREATE VIEW most_popular_articles_ever AS
      (SELECT count,
              articles.title
       FROM articles
       JOIN
         (SELECT count(*) AS count, substring(path FROM 10) AS article_log
          FROM log
          WHERE status='200 OK'
            AND path LIKE '/article/%'
          GROUP BY path
          ORDER BY count DESC
          LIMIT 3) sub ON article_log = articles.slug);

### Who are the most popular article authors of all time?
    CREATE VIEW most_popular_authors AS
      (SELECT count, authors.name
       FROM authors
       JOIN
         (SELECT count(*) AS count, author
          FROM articles
          JOIN
            (SELECT substring(path FROM 10) AS article
             FROM log
             WHERE status='200 OK'
               AND path LIKE '/article/%') sub ON articles.slug = article
          GROUP BY author) sub2 ON authors.id = author);

### On which days did more than 1% of requests lead to errors?
    CREATE VIEW requests_error AS
      (SELECT t1.day,
              round((100*failed_requests::float/requests)::DECIMAL, 2) AS fails
       FROM
         (SELECT date_trunc('day', TIME)::date AS "day", count(*) AS "requests"
          FROM log
          GROUP BY 1) t1
       JOIN
         (SELECT date_trunc('day', TIME)::date AS "day", count(*) AS "failed_requests"
          FROM log
          WHERE STATUS != '200 OK'
          GROUP BY 1) t2 ON (t1.day = t2.day)
       WHERE round((100*failed_requests::float/requests)::DECIMAL, 2) > 1);