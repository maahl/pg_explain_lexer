# Postgres EXPLAIN lexer

This is a custom [Pygments](http://pygments.org/) lexer for coloring the output
of PostgreSQL's `EXPLAIN ANALYZE` command.

See [the tests output](test/test.pdf) for an example of how it looks.

## Limitations

This has only been tested for Latex output, with only one Pygments style 
(colorful), and has been made to look good only with that theme.

The type of the tokens has been chosen to make something that looks good, not
for the semantics; for example, the numbers are displayed using Name.Literal
instead of Number.Integer, just because it looks better.

Only the output of "EXPLAIN ANALYZE" is handled, no other options have been
tested.

## Usage

```
pygmentize -l pg_explain_lexer.py:PgExplainLexer -x <(psql -c "EXPLAIN ANALYZE SELECT count(*) FROM pg_class;")
```

If you notice a pygments error (an unhandled case), please open an issue and
post your EXPLAIN plan with the error.
