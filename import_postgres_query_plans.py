#!/usr/bin/env python3

# this script retrieves all the query plans found in postgresql's regression
# tests, and generates a latex file containing them all

import os
import re
import sys

OUTPUT_FILE = os.path.join('test', 'postgres_regress.tex')

if __name__ == '__main__':
    try:
        postgres_path = sys.argv[1]
    except IndexError:
        print('Path to postgresql source directory must be passed as argument')
        print('Example: import_postgres_query_plans ~/projects/postgresql')
        exit(1)

    # get the list of .out files in postgresql's source
    out_files = []
    for root, dirs, files in os.walk(os.path.join(postgres_path, 'src', 'test')):
        out_files += [os.path.join(root, f) for f in files if f.endswith('.out')]

    # get the query plans
    query_plans = []
    # query_plan_regex = re.compile(r'^\s*QUERY PLAN\s*\n(.*?\n)+?\(\d+ row(s)?\)')
    query_plan_regex = re.compile(r' *QUERY PLAN *\n.*?\n\(\d+ rows?\)\n', re.DOTALL)
    for f in out_files:
        with open(f) as content:
            try:
                query_plans += query_plan_regex.findall(content.read())
            except UnicodeDecodeError:
                # ignore files not in unicode
                pass

    os.remove(OUTPUT_FILE)
    with open(OUTPUT_FILE, 'w') as f:
        f.write('''\documentclass{article}

\\usepackage[margin=0.5cm]{geometry}
\\paperwidth=\dimexpr \paperwidth + 2cm\\relax
\\usepackage{minted}
\\usemintedstyle{colorful}

\\newenvironment{queryplan}[1]{
    \VerbatimEnvironment%
    \\begin{listing}
        \caption{#1}
        \\begin{minted}[frame=lines, framesep=2mm, fontsize=\\footnotesize]{../pg_explain_lexer.py:PgExplainLexer -x}}{%
        \end{minted}
    \end{listing}
}

\\begin{document}

''')
        for i, qp in enumerate(query_plans):
            f.write('\\begin{queryplan}{query plan ' + str(i) + '}\n')
            f.write(qp)
            f.write('\end{queryplan}\n\n')
            # add a \clearpage every couple of plans to force latex to process
            # the floats
            if (i+1) % 20 == 0:
                f.write('\clearpage\n\n')

        f.write('\end{document}\n')
