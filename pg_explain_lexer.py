from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import *


class PgExplainLexer(RegexLexer):
    name = 'Postgres Explain'
    aliases = ['pg_explain']
    filenames = []

    tokens = {
        'root': [
            (r'(\s+|:|\(|\)|ms|kB|->|\.\.)', Punctuation),
            (r'(cost=|rows=|width=|loops=|time=|actual|Memory)', Comment.Single),
            (r'(Sort Key)(: )', bygroups(Comment.Preproc, Punctuation), 'object_name'),
            (r'(Join Filter|Filter|Merge Cond)(: \()(.*?)(\))', bygroups(
                Comment.Preproc,
                Punctuation,
                Name.Variable.Instance,
                Punctuation,
            )),
            (r'Seq Scan on ', Keyword.Type, 'object_name'),
            (r'(Index Scan using )(\w)( on )', bygroups(Keyword.Type, 'object_name', Keyword.Type), 'object_name'),
            (r'(Sort Method|Join Filter|Rows Removed by Join Filter|Rows Removed by Filter|Planning Time|Execution Time)', Comment.Preproc),
            (r'(Sort|Nested Loop|Seq Scan on|Merge Join|Index Scan using)', Keyword.Type),
            # strings
            (r"'(''|[^'])*'", String.Single),
            # numbers
            (r'[0-9]+(\.[0-9]+)?', Name.Literal),
            # explain header
            (r'\s*QUERY PLAN', Comment.Single),
            (r'-+', Comment.Single),
        ],
        'object_name': [
            # matches possibly schema-qualified table and column names
            (r'\w+(\.\w+)*', Name.Variable.Instance),
        ],
    }
