from pygments.lexer import RegexLexer, words, bygroups
from pygments.token import *


class PgExplainLexer(RegexLexer):
    name = 'Postgres Explain'
    aliases = ['pg_explain']
    filenames = []

    tokens = {
        'root': [
            (r'(\s+|:|\(|\)|ms|kB|->|\.\.)', Punctuation),
            (r'(cost=|rows=|width=|loops=|time=|exact=|actual|Memory Usage|Memory|Buckets|Batches|originally|rows)', Comment.Single),
            (r'(Sort Key)(: )', bygroups(Comment.Preproc, Punctuation), 'object_name'),
            (r'(Sort Method)(: )', bygroups(Comment.Preproc, Punctuation), 'object_name'),
            (r'(Join Filter|Filter|Merge Cond|Hash Cond|Index Cond|Recheck Cond)(: )', bygroups(Comment.Preproc, Punctuation), 'predicate'),
            (r'(Parallel )?Seq Scan on |(Parallel )?Bitmap Heap Scan on |Bitmap Index Scan on |Subquery Scan on ', Keyword.Type, 'object_name'),
            # "using" operators
            (r'((?:Parallel )?Index (?:Only )?Scan using )(\w+(?:\.\w+)*)( on )', bygroups(Keyword.Type, Name.Variable, Keyword.Type), 'object_name'),
            # operator arguments or details
            (r'(Sort Method|Join Filter|Rows Removed by Join Filter|Rows Removed by Filter|Planning Time|Execution Time|Heap Fetches|Heap Blocks|Workers (Planned|Launched)|never executed)', Comment.Preproc),
            # simple keywords
            (r'(Sort|Nested Loop Left Join|Nested Loop|Merge Join|Hash (Right|Left|Full) Join|(Parallel )?Hash Join|(Parallel )?Hash|Limit|(Finalize |Partial )?Aggregate|Materialize|Gather( Merge)?)|(Merge )?Append', Keyword.Type),
            # strings
            (r"'(''|[^'])*'", String.Single),
            # numbers
            (r'[0-9]+(\.[0-9]+)?', Name.Literal),
            # explain header
            (r'\s*QUERY PLAN\s*\n-+', Comment.Single),
        ],
        'expression': [
            # matches any kind of parenthesized expression
            # the first opening paren is matched by the 'caller'
            (r'\(', Punctuation, 'expression'),
            (r'\)', Punctuation, '#pop'),
            (r'[^)]*', Name.Variable),
        ],
        'object_name': [
            # matches possibly schema-qualified table and column names
            # if object_name is parenthesized, mark opening paren as
            # punctuation, call 'expression', and exit state
            (r'\(', Punctuation, 'expression'),
            (r'\)', Punctuation, '#pop'),
            (r'\w+(\.\w+)*( USING \S+| \w+ USING \S+| \w)?', Name.Variable),
            (r'', Punctuation, '#pop'),
        ],
        'predicate': [
            # if predicate is parenthesized, mark paren as punctuation
            (r'(\()([^\n]*)(\))', bygroups(Punctuation, Name.Variable, Punctuation), '#pop'),
            # otherwise color until newline
            (r'[^\n]*', Name.Variable, '#pop'),
        ]
    }
