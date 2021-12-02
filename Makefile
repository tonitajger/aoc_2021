.PHONY: download_inputs
download_inputs:
	python tools/download_inputs.py

# usage: make create_day day=1
.PHONY: create
create:
	cp -a -n templates/template_day/. days/day$(day)

# usage: make download_create_day day=1
.PHONY: download_create
download_create: download_input create

# usage: make run_day day=1
.PHONY: run
run:
	python days/day$(day)/main.py

