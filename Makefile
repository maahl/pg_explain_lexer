test:
	cd test && xelatex -shell-escape test.tex && rm -r _minted-test

.PHONY: test
