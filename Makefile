test:
	cd test && xelatex -shell-escape test.tex && rm -r _minted-test

test-regress:
	./import_postgres_query_plans.py $(POSTGRES_DIR) && cd test && xelatex -shell-escape postgres_regress.tex && rm -r _minted-postgres_regress

.PHONY: test
