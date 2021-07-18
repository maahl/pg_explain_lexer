#!/usr/bin/env python3

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import PostgresLexer
import click
import re
import sys

from pg_explain_lexer import PgExplainLexer

# regex for matching timestamps, such as '2021-07-17 16:40:56.675 '
TIMESTAMP_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3} ")


@click.command()
@click.option(
    "--sql-style", default="default", help="Pygments style to use for SQL statements"
)
@click.option(
    "--explain-style", default="default", help="Pygments style to use for query plans"
)
def prettify_logs(sql_style, explain_style):
    sql_lexer = PostgresLexer()
    explain_lexer = PgExplainLexer()
    sql_formatter = Terminal256Formatter(style=sql_style)
    explain_formatter = Terminal256Formatter(style=explain_style)
    # auto_explain shows the query before the plan, so we have 3 states:
    # * "normal": normal log lines, not colorized
    # * "reading_query": query log lines, colorized with SQL formatter
    # * "reading_plan": explain log lines, colorized with our custom formatter
    #
    # state transitions are:
    # * normal -> reading_query
    # * reading_query -> reading_plan
    # * reading_plan -> normal
    reading_query = False
    reading_plan = False
    schedule_transition_to_reading_plan = False
    while True:
        line = sys.stdin.readline().strip("\n")

        # when in the normal state
        if not reading_query and not reading_plan:
            # check if we start reading a query
            if line.strip().startswith("Query Text: "):
                reading_query = True
                # we don't want to colorize "query text" so print it beforehand
                print("\tQuery Text: ", end="")
                line = line[13:]

        # when in the reading_query state
        # this is not an "elif" so that we can detect single-line queries
        if reading_query:
            # if we detect the end of a query (this can break for some queries)
            if line.endswith(";"):
                # we want to transition to the next state, but only after
                # printing this line
                schedule_transition_to_reading_plan = True

        # when in the reading_plan state
        elif reading_plan:
            # if the line starts with a timestamp, it is a normal log line
            if TIMESTAMP_REGEX.match(line):
                reading_plan = False

        # print the line with the proper formatting
        if reading_query:
            print(highlight(line, sql_lexer, sql_formatter), end="")
        elif reading_plan:
            print(highlight(line, explain_lexer, explain_formatter), end="")
        else:
            print(line)

        # process any transition that needs to happen after printing the line
        if schedule_transition_to_reading_plan:
            reading_query = False
            reading_plan = True
            schedule_transition_to_reading_plan = False


if __name__ == "__main__":
    try:
        prettify_logs()
    except KeyboardInterrupt:
        sys.exit()
