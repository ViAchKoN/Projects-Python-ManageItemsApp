# if BIN not provided, try to detect the binary from the environment
PYTHON_INSTALL := $(shell python3 -c 'import sys;print(sys.executable)')
BIN ?= $(shell [ -e `pwd`/.venv/bin ] && echo `pwd`/'.venv/bin' || dirname $(PYTHON_INSTALL))/

CODE = application

help:  ## This help dialog.
	@IFS=$$'\n' ; \
	help_lines=(`fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##/:/'`); \
	printf "%-15s %s\n" "target" "help" ; \
	printf "%-15s %s\n" "------" "----" ; \
	for help_line in $${help_lines[@]}; do \
		IFS=$$':' ; \
		help_split=($$help_line) ; \
		help_command=`echo $${help_split[0]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		help_info=`echo $${help_split[2]} | sed -e 's/^ *//' -e 's/ *$$//'` ; \
		printf '\033[36m'; \
		printf "%-15s %s" $$help_command ; \
		printf '\033[0m'; \
		printf "%s\n" $$help_info; \
	done

test:	## Start tests
	$(BIN)python -m pytest $(CODE) $(args)

lint:	## Code linting
	$(BIN)flake8 --jobs 4 $(CODE)
	$(BIN)brunette --config=setup.cfg --check $(CODE) --exclude $(CODE)/migrations $(CODE)/tests

pretty:  ## Auto-format code
	$(BIN)isort $(CODE) tests
	$(BIN)brunette --config=setup.cfg $(CODE) --exclude $(CODE)/migrations $(CODE)/tests
