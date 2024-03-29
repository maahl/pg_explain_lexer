**Note: this repository is deprecated**

Thanks to @anayrat, this is now included in pygments, changes should be made
there. See [here](https://github.com/pygments/pygments/pull/2398)


# Postgres EXPLAIN lexer

This is a custom [Pygments](http://pygments.org/) lexer for coloring the output
of PostgreSQL's `EXPLAIN ANALYZE` command.

See [the tests output](test/test.pdf) for an example of how it looks.

## Limitations

This has only been tested for Latex output, with only one Pygments style
(colorful), and has been made to look good only with that theme.

The type of the tokens has been chosen to make something that looks good, not
for the semantics; for example, the numbers are displayed using Generic.Strong
instead of Number.Integer, just because it looks better.

Only the output of "EXPLAIN ANALYZE" is handled, no other options have been
tested.

## Usage

```
pygmentize -0 style=autumn -l pg_explain_lexer.py:PgExplainLexer -x <(psql -c "EXPLAIN ANALYZE SELECT count(*) FROM pg_class;")
```

Adjust the style argument if the colors are unreadable or if you don't like them.

For a single psql session:
```
\set color '\\g |pygmentize -l ~/projects/pg_explain_lexer/pg_explain_lexer.py:PgExplainLexer -x'
```

You can then color the explain output directly from psql, by replacing the
trailing semicolon with `:color`
```
EXPLAIN ANALYZE SELECT * FROM customers :color
```

Or if you want the output to always be colored when explaining queries, put this
in your .psqlrc:

```
\pset pager always
\setenv PAGER '{ IFS= read -r line; if echo "$line" | grep -q "QUERY PLAN"; then pygmentize -l ~/projects/pg_explain_lexer/pg_explain_lexer.py:PgExplainLexer -x <<<$(printf "%s\n%s" "$line" "$(cat)"); else less <<<$(printf "%s\n%s" "$line" "$(cat)"); fi }'
```

This ugly one-liner detects if the output is a query plan. If yes, it sends it
to pygmentize for coloring; otherwise it calls your usual pager (`less` in this
example).

If you notice a pygments error (an unhandled case), please open an issue and
post your EXPLAIN plan with the error.

## Colorize auto_explain output in logs

A wrapper script is provided, that will apply syntax highlighting to SQL queries and their plan output by the auto_explain extension.

```
tail -f postgresql.log | ./colorize_plans_in_logs.py --sql-style=colorful --explain-style=autumn
```

The style options are Pygments styles, adjust them if the colors are unreadable or if you don't like them.
You need to have the click python package installed, you can install it with `pip install -r requirements.txt`.

## Testing

The `import_postgres_query_plans.py` script retrieves all the query plans
expected as output in postgresql's regression tests, and generates a latex file
with all of them.
To generate the pdf:
```
make test-regress POSTGRES_DIR=~/projects/postgresql
```
